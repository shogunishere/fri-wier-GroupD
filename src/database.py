import psycopg2
import psycopg2.extras

from contextlib import contextmanager
from settings import DATABASE

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

def insert_link(from_page_id, page_id):
    with db_connect() as conn:
        with get_cursor(conn) as cursor:
            query = """
            INSERT INTO crawldb.link (from_page, to_page)
            VALUES (%s, %s);
            """

            cursor.execute(query, (from_page_id, page_id))

            return page_id

def get_site(domain):
    with db_connect() as conn:
            with get_cursor(conn) as cursor:
                query = """
                SELECTE id FROM crawldb.site WHERE domain = %s;
                """

                cursor.execute(query, (domain))

                return cursor.fetchone()['id']

def insert_site(domain, robots_content, sitemap_content):
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
        
def insert_image(page_id, filename, content_type, data, accessed_time):
    with db_connect() as conn:
        with get_cursor(conn) as cursor:
            query = """
            INSERT INTO crawldb.image (page_id, filename, content_type, data, accessed_time)
            VALUES (%s, %s, %s, %s, %s) RETURNING id;
            """

            cursor.execute(query, (page_id, filename, content_type, data, accessed_time))

            return cursor.fetchone()['id']



