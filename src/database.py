import psycopg2
import psycopg2.extras

from contextlib import contextmanager
from settings import DATABASE
from utils import remove_null_characters

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

def get_site(domain):
    with db_connect() as conn:
        with get_cursor(conn) as cursor:
            query = """
            SELECT id FROM crawldb.site WHERE domain = %s;
            """

            cursor.execute(query, (domain,))

            result = cursor.fetchone()

            if result is not None:
                return result[0] 
            else:
                return None 
                

def get_page(url):
    with db_connect() as conn:
        with get_cursor(conn) as cursor:
            query = """
            SELECT id FROM crawldb.page WHERE url = %s;
            """

            cursor.execute(query, (url,))

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
                
def insert_link(from_page_id, page_id):
    with db_connect() as conn:
        with get_cursor(conn) as cursor:
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
            query = """
            INSERT INTO crawldb.site (domain, robots_content, sitemap_content)
            VALUES (%s, %s, %s) RETURNING id;
            """

            cursor.execute(query, (domain, robots_content, sitemap_content))

            return cursor.fetchone()['id']

def insert_page(site_id, page_type_code, url, html_content, http_status_code, accessed_time):
    with db_connect() as conn:
        with get_cursor(conn) as cursor:
            query = """
            INSERT INTO crawldb.page (site_id, page_type_code, url, html_content, http_status_code, accessed_time)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
            """

            cursor.execute(query, (site_id, page_type_code.name, url, html_content, http_status_code, accessed_time))

            return cursor.fetchone()['id']

def insert_binary(page_id, data_type_code, data):
    with db_connect() as conn:
        with get_cursor(conn) as cursor:
            query = """
            INSERT INTO crawldb.page_data (page_id, data_type_code, data)
            VALUES (%s, %s, %s) RETURNING id;
            """

            cursor.execute(query, (page_id, data_type_code, data, ))

            return cursor.fetchone()['id']

def insert_image(page_id, filename, content_type, data, accessed_time):
    with db_connect() as conn:
        with get_cursor(conn) as cursor:
            query = """
            INSERT INTO crawldb.image (page_id, filename, content_type, data, accessed_time)
            VALUES (%s, %s, %s, %s, %s) RETURNING id;
            """

            cursor.execute(query, (page_id, filename, content_type, data, accessed_time))

            return cursor.fetchone()['id']



