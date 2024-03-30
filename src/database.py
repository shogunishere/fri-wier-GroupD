import psycopg2
from psycopg2.extras import execute_values
from contextlib import contextmanager
from datetime import datetime
import threading

from settings import DATABASE
from utils import get_domain, get_url_path, remove_null_characters
from models import PageType


lock = threading.Lock()


@contextmanager
def db_connect():
    conn = psycopg2.connect(
        host=DATABASE['host'],
        port=DATABASE['port'],
        dbname=DATABASE['dbname'],
        user=DATABASE['user'],
        password=DATABASE['password'])
    try:
        yield conn
    except Exception as e:
        conn.rollback()
        raise e
    else:
        conn.commit()
    finally:
        conn.close()

@contextmanager
def get_cursor(connection):
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        yield cursor
    finally:
        cursor.close()


def start_frontier():
    with db_connect() as conn:  
        with conn.cursor() as cursor:
            with lock:
                select_query = """
                    SELECT id, url
                    FROM crawldb.page 
                    WHERE in_progress != TRUE AND page_type_code = 'FRONTIER'
                    ORDER BY accessed_time ASC
                    LIMIT 1;
                """
                cursor.execute(select_query)
                result = cursor.fetchone()

                if result:
                    frontier_id = result[0]
                    update_query = """
                        UPDATE crawldb.page SET in_progress = TRUE
                        WHERE id = %s;
                    """
                    cursor.execute(update_query, (frontier_id,))
                    conn.commit()  # Committing the transaction

                    return result  # Returning the entire row
                else:
                    return None, None



def finish_frontier(frontier_id, page_type, status_code):
    with db_connect() as conn:
        with conn.cursor() as cursor:
            with lock:
                query = "UPDATE crawldb.page SET "
                params = []

                if page_type is not None:
                    query += "page_type_code = %s, "
                    params.append(page_type.name)

                query += "in_progress = %s, http_status_code = %s WHERE id = %s RETURNING id;"
                params.extend([False, status_code, frontier_id])

                cursor.execute(query, tuple(params))

                result = cursor.fetchone()
                return result[0] if result else None
            

def get_site(domain):
    with db_connect() as conn:
        with get_cursor(conn) as cursor:
            query = """
            SELECT id FROM crawldb.site WHERE domain = %s;
            """

            cursor.execute(query, (domain, ))

            result = cursor.fetchone()

            if result is not None:
                return result[0] 
            else:
                return None 
                

def get_page_by_url(url):
    domain = get_domain(url)
    url_path = get_url_path(url)

    with db_connect() as conn:
        with get_cursor(conn) as cursor:
            query = """
            SELECT crawldb.page.id FROM crawldb.page 
            LEFT JOIN crawldb.site 
            ON crawldb.site.id = crawldb.page.site_id
            WHERE (crawldb.site.domain = %s AND crawldb.page.url = %s) OR crawldb.page.url = %s;
            """

            cursor.execute(query, (domain, url_path, url))

            result = cursor.fetchone()

            if result is not None:
                return result[0] 
            else:
                return None
                

def get_rules(site_id):
    with db_connect() as conn:
        with get_cursor(conn) as cursor:
            query = """
            SELECT robots_content FROM crawldb.site WHERE id = %s;
            """

            cursor.execute(query, (site_id,))

            result = cursor.fetchone()

            if result is not None:
                return result[0] 
            else:
                return None
                

def get_last_accessed_time(site_id):
    with db_connect() as conn:
        with get_cursor(conn) as cursor:
            query = "SELECT last_accessed_time FROM crawldb.site WHERE id = %s;"
            cursor.execute(query, (site_id,))
            result = cursor.fetchone()
        
        if result is not None:
            return result[0]
        else:
            return None
        

def get_duplicate_html(html_hash):
    with db_connect() as conn:  # Replace db_connect with your actual database connection function
        with conn.cursor() as cursor:
            query = "SELECT COUNT(*) FROM crawldb.page WHERE html_hash = %s;"
            cursor.execute(query, (html_hash,))
            count = cursor.fetchone()[0]
            return count > 0
        

def insert_link(from_page_id, page_id):
    if from_page_id is None:
        return None
    
    with db_connect() as conn:
        with get_cursor(conn) as cursor:
            with lock:
                query = """
                INSERT INTO crawldb.link (from_page, to_page)
                VALUES (%s, %s);
                """

                cursor.execute(query, (from_page_id, page_id))

                return page_id

def insert_site(domain, robots_content, sitemap_content):
    robots_content = remove_null_characters(robots_content)
    sitemap_content = remove_null_characters(sitemap_content)

    with db_connect() as conn:
        with get_cursor(conn) as cursor:
            with lock:
                query = """
                INSERT INTO crawldb.site (domain, robots_content, sitemap_content)
                VALUES (%s, %s, %s) RETURNING id;
                """

                cursor.execute(query, (domain, robots_content, sitemap_content))

                return cursor.fetchone()['id']

def insert_frontier(url, accessed_time):
    with db_connect() as conn:
        with get_cursor(conn) as cursor:
            with lock:
                query = """
                INSERT INTO crawldb.page (site_id, page_type_code, url, html_content, http_status_code, in_progress, accessed_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;
                """

                cursor.execute(query, (None, PageType.FRONTIER.name, url, None, None, False, accessed_time))

                return cursor.fetchone()['id']


def insert_page(site_id, page_type_code, url, html_content, http_status_code, accessed_time):
    with db_connect() as conn:
        with get_cursor(conn) as cursor:
            with lock:
                query = """
                INSERT INTO crawldb.page (site_id, page_type_code, url, html_content, http_status_code, accessed_time)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
                """

                cursor.execute(query, (site_id, page_type_code.name, url, html_content, http_status_code, accessed_time))

                return cursor.fetchone()['id']


def insert_binary(page_id, binary_type_code, data):
    with db_connect() as conn:
        with get_cursor(conn) as cursor:
            with lock:
                query = """
                INSERT INTO crawldb.page_data (page_id, data_type_code, data)
                VALUES (%s, %s, %s) RETURNING id;
                """

                cursor.execute(query, (page_id, binary_type_code.name, data, ))

                return cursor.fetchone()['id']


def insert_image(page_id, filename, content_type, data, accessed_time):
    with db_connect() as conn:
        with get_cursor(conn) as cursor:
            with lock:
                query = """
                INSERT INTO crawldb.image (page_id, filename, content_type, data, accessed_time)
                VALUES (%s, %s, %s, %s, %s) RETURNING id;
                """

                cursor.execute(query, (page_id, filename, content_type, data, accessed_time))

                return cursor.fetchone()['id']


def update_page(page_id, site_id, url, page_type, html, html_hash, http_status_code, accessed_time):
    with db_connect() as conn:
        with get_cursor(conn) as cursor:
            with lock:
                query = """
                UPDATE crawldb.page 
                SET site_id = %s, url = %s, page_type_code = %s, html_content = %s, html_hash = %s, http_status_code = %s, accessed_time = %s
                WHERE id = %s
                RETURNING id;
                """

                cursor.execute(query, (site_id, url, page_type.name, html, html_hash, http_status_code, accessed_time, page_id))

                result = cursor.fetchone()
                return result[0] if result else None
        

def update_frontier_in_progress(frontier_id, in_progress):
    with db_connect() as conn:
        with conn.cursor() as cursor:
            with lock:
                query = """
                UPDATE crawldb.page SET in_progress = %s
                WHERE id = %s
                RETURNING id;
                """
                cursor.execute(query, (in_progress, frontier_id))

                result = cursor.fetchone()
                return result[0] if result else None


def update_site_time(site_id, current_time):
    with db_connect() as conn:
        with conn.cursor() as cursor:
            with lock:
                query = """
                UPDATE crawldb.site SET last_accessed_time = %s
                WHERE id = %s
                RETURNING id;
                """
                cursor.execute(query, (current_time, site_id))

                result = cursor.fetchone()
                return result[0] if result else None


# Bulk operations


def bulk_check_existing_urls(urls):
    # Prepare the data for the query as a list of tuples (url, domain, url_path)
    query_data = [(url, get_domain(url), get_url_path(url)) for url in urls]

    if not query_data:
        return set()

    # Construct the query using a CTE for better readability and performance
    query = """
    WITH input_urls(url, domain, url_path) AS (VALUES %s)
    SELECT input_urls.url
    FROM input_urls
    JOIN crawldb.page p ON input_urls.url = p.url
    UNION
    SELECT input_urls.url
    FROM input_urls
    JOIN crawldb.page p ON input_urls.url_path = p.url
    JOIN crawldb.site s ON input_urls.domain = s.domain;
    """

    existing_urls = set()
    with db_connect() as conn:
        with get_cursor(conn) as cursor:
            # Using execute_values to handle the insertion of multiple rows into the CTE
            execute_values(cursor, query, query_data, template=None, page_size=100)
            existing_urls = {row[0] for row in cursor.fetchall()}
    return existing_urls


def bulk_insert_frontier(urls, current_time):
    if not urls:
        return []

    with lock:
        print(f"Starting bulk insert")

        try:
            existing_urls = bulk_check_existing_urls(urls)
            values_to_insert = [
                (None, PageType.FRONTIER.name, url, None, None, False, current_time) 
                for url in urls if url not in existing_urls
            ]

            if not values_to_insert:
                print(f"Ended bulk insert")
                return []

            with db_connect() as conn:
                with get_cursor(conn) as cursor:
                    # Create a temporary table to hold returned ids
                    cursor.execute("CREATE TEMP TABLE tmp_ids(id INTEGER)")

                    # Construct a query with multiple values and RETURNING clause
                    query = """
                    WITH ins AS (
                        INSERT INTO crawldb.page (
                            site_id, page_type_code, url, 
                            html_content, http_status_code, 
                            in_progress, accessed_time
                        )
                        VALUES %s
                        RETURNING id
                    )
                    INSERT INTO tmp_ids
                    SELECT id FROM ins;
                    """
                    # Execute the bulk insert
                    execute_values(cursor, query, values_to_insert)

                    # Retrieve the generated ids
                    cursor.execute("SELECT id FROM tmp_ids")
                    frontier_ids = [row[0] for row in cursor.fetchall()]

                    # Drop the temporary table
                    cursor.execute("DROP TABLE tmp_ids")

            print(f"Ended bulk insert")
            return frontier_ids

        except psycopg2.DatabaseError as e:
            print(f"Ended bulk insert")

            print(f"Database error occurred: {e}")
            # Optionally, re-raise the exception if you want the caller to handle it
            # raise

        except Exception as e:
            print(f"Ended bulk insert")
            
            print(f"An error occurred: {e}")
            # Optionally, re-raise the exception if you want the caller to handle it
            # raise


def bulk_insert_link(from_page_id, frontier_ids):
    if from_page_id is None or frontier_ids is None == 0:
        return
    
    from_page_ids = [from_page_id] * len(frontier_ids)
    values_to_insert = list(zip(from_page_ids, frontier_ids))

    with db_connect() as conn:
        with get_cursor(conn) as cursor:
                # Construct a query with multiple values
                query = "INSERT INTO crawldb.link (from_page, to_page) VALUES %s;"
                template = "(%s, %s)"

                execute_values(cursor, query, values_to_insert, template) 

    