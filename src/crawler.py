
from datetime import datetime
from collections import deque

from driver import get_driver
from database import insert_site, insert_page, insert_link
from utils import get_domain, get_http_headers, get_urls, fetch_robots_txt, fetch_sitemap
from models import PageType

def crawl(seed_urls, depth):
    driver = get_driver()

    queue = deque([(None, url, 1) for url in seed_urls]) # Double ended queue (FIFO)

    while queue:
        from_page_id, url, current_depth = queue.popleft()  
        if current_depth > depth:
            break # Break out if maximum depth is exceeded

        # Start retrieving
        print(f"Retrieving page URL '{url}' at depth {current_depth}")
        accessed_time = datetime.now()

        # Get content
        driver.get(url)
        html = driver.page_source

        # TODO: check hash
        
        # Get headers with a new request
        status_code, page_type_code = get_http_headers(url)

        # Process site
        domain = get_domain(url)
        site_id = process_site(domain)
        
        # Process page
        page_id = process_page(url, site_id, status_code, page_type_code, html, accessed_time)
        if (from_page_id): insert_link(from_page_id, page_id)

        # Populate queue with newly found URLs
        new_urls = get_urls(html, url)
        for new_url in new_urls:
            queue.append((page_id, new_url, current_depth + 1))

    driver.quit()

def process_site(domain):
    robots_txt = fetch_robots_txt(domain)
    sitemap = fetch_sitemap(domain)

    site_id = insert_site(domain, robots_txt, sitemap)

    print(f"New site [id: {site_id}]")

    return site_id

def process_page(url, site_id, status_code, page_type_code, html, accessed_time):
    page_id = insert_page(site_id, page_type_code, url, html, status_code, accessed_time)

    print(f"New page [id: {page_id}]")

    return page_id






# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver.common.by import By
# import concurrent.futures
# import threading
# import psycopg2
# from dotenv import load_dotenv
# import os

# WEB_PAGE_ADDRESS = "https://vreme.arso.gov.si"
# WEB_DRIVER_LOCATION = "./driver/chromedriver.exe"  
# TIMEOUT = 5

# chrome_options = ChromeOptions()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument("user-agent=fri-ieps-TEST")

# print(f"Retrieving web page URL '{WEB_PAGE_ADDRESS}'")

# service = ChromeService(executable_path=WEB_DRIVER_LOCATION)
# driver = webdriver.Chrome(service=service, options=chrome_options)

# driver.get(WEB_PAGE_ADDRESS)

# # Timeout needed for Web page to render (read more about it)
# time.sleep(TIMEOUT)

# html = driver.page_source

# print(f"Retrieved Web content (truncated to first 900 chars): \n\n'{html[:900]}'\n")

# page_msg = driver.find_element(By.CSS_SELECTOR, ".panel-header")

# print(f"Web page message: '{page_msg.text}'")

# driver.close()

# # db

# lock = threading.Lock()

# load_dotenv()

# database_host = os.getenv('DB_HOST')
# database_password = os.getenv('DB_PASSWORD')
# database_user = os.getenv('DB_USER')
# database_name = os.getenv('DB_NAME')
# database_port = os.getenv('DB_PORT')

# def reset_db_values():
#     conn = psycopg2.connect(host=database_host, port = database_port, dbname=database_name, user=database_user, password=database_password)
#     conn.autocommit = True
    
#     cur = conn.cursor()
#     cur.execute("UPDATE showcase.counters SET value = 0")
    
#     cur.close()
#     conn.close()
    
# def print_db_values():
#     conn = psycopg2.connect(host=database_host, port = database_port, dbname=database_name, user=database_user, password=database_password)
#     conn.autocommit = True

#     print("\nValues in the database:")
#     cur = conn.cursor()
#     cur.execute("SELECT counter_id, value FROM showcase.counters ORDER BY counter_id")
#     for counter_id, value in cur.fetchall():
#         print(f"\tCounter id: {counter_id}, value: {value}")
#     cur.close()
#     conn.close()

# def increase_db_values(counter_id, increases):
#     conn = psycopg2.connect(host=database_host, port = database_port, dbname=database_name, user=database_user, password=database_password)
#     conn.autocommit = True
    
#     for i in range(increases):
#         cur = conn.cursor()
#         cur.execute("SELECT value FROM showcase.counters WHERE counter_id = %s", \
#                     (counter_id,))
#         value = cur.fetchone()[0]
#         cur.execute("UPDATE showcase.counters SET value = %s WHERE counter_id = %s", \
#                     (value+1, counter_id))
#         cur.close()
#     conn.close()
    
# def increase_db_values_locking(counter_id, increases):
#     conn = psycopg2.connect(host=database_host, port = database_port, dbname=database_name, user=database_user, password=database_password)
#     conn.autocommit = True
    
#     for i in range(increases):
#         with lock:
#             cur = conn.cursor()
#             cur.execute("SELECT value FROM showcase.counters WHERE counter_id = %s", \
#                         (counter_id,))
#             value = cur.fetchone()[0]
#             cur.execute("UPDATE showcase.counters SET value = %s WHERE counter_id = %s", \
#                         (value+1, counter_id))
#             cur.close()
#     conn.close()

# reset_db_values()
# print_db_values()

# with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
#     print(f"\n ... executing workers ...\n")
#     for _ in range(3):
#         executor.submit(increase_db_values, 1,1000)
#     for _ in range(3):
#         executor.submit(increase_db_values_locking, 2,1000)
    
# print_db_values()
