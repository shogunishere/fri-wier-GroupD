
from datetime import datetime
from collections import deque

from driver import get_driver
from database import get_site, get_page, get_rules, insert_site, insert_page, insert_link, insert_binary, insert_image
from utils import get_domain, get_base_url, get_url_path, fetch_http_headers, get_urls, fetch_images, fetch_robots_txt, fetch_sitemap, parse_robots_txt, parse_sitemap, is_url_allowed
from models import PageType

from urllib.parse import urlparse

import threading
from queue import Queue, Empty

def crawl(user_agent, seed_urls, depth, num_threads):

    print(f"num_threads: {num_threads}")

    queue = Queue() # Queue from the Python standard library for thread-safe queueing

    for url in seed_urls:
        queue.put((None, url, 1))  # (from_page_id, url, current_depth)

    # List to hold all the worker threads
    threads = []

    for i in range(num_threads):
        thread_name = f"Worker-{i+1}"
        thread = threading.Thread(target=thread_worker, name=thread_name, args=(user_agent, queue, depth))
        threads.append(thread)
        thread.start()

    queue.join()

    for thread in threads:
        thread.join()

def process_site(base_url, user_agent):

    domain = get_domain(base_url)

    site_id = get_site(domain)

    # Check if already exists
    if (site_id is None):
        # Fetch robots.txt 
        robots_txt = fetch_robots_txt(base_url)
        rules = parse_robots_txt(robots_txt, user_agent)

        # Fetch sitemap if exists
        sitemap = None
        sitemap_urls = []
        if rules is not None and rules["Sitemap"]:
            sitemap = fetch_sitemap(base_url, rules["Sitemap"])
            sitemap_urls = parse_sitemap(sitemap)

        site_id = insert_site(domain, robots_txt, sitemap)

        print(f"New site [id: {site_id}]")

        return site_id, rules, sitemap_urls

    else:
        robots_txt = get_rules(site_id)
        rules = parse_robots_txt(robots_txt, user_agent)

        print(f"Existing site [id: {site_id}]")

        return site_id, rules, []

def process_page(url, site_id, status_code, page_type_code, html, accessed_time):

    # TODO: check hash for duplicates

    page_id = get_page(url)

    # Check if already exists
    if (page_id is None):
        page_id = insert_page(site_id, page_type_code, url, html, status_code, accessed_time)
        print(f"New page [id: {page_id}]")

        # Binary
        if (page_type_code == PageType.BINARY):
            binary_id = insert_binary(page_id, None, None) # Not adding binary data
            print(f"New binary [id: {binary_id}]")

        return page_id
    else:
        print(f"Existing page [id: {page_id}]")
        return None

def process_image(page_id, filename, content_type, data, accessed_time):
    image_id = insert_image(page_id, filename, content_type, data, accessed_time)
    print(f"New image [filename: {filename}]")

def fetch_and_process_url(url, user_agent, worker_id, depth):
    print(f"Worker {worker_id}: Processing {url} with user agent {user_agent}")
    print(f"Retrieving page URL '{url}' at depth {depth}")

    print(f"Retrieving page URL '{url}' at depth {depth}")
    accessed_time = datetime.now()

    parsed_url = urlparse(url)
    if parsed_url.scheme not in ['http', 'https']:
        print(f"Skipping non-HTTP(S) URL: {url}")
        return

    # Make http head request
    status_code, page_type_code = fetch_http_headers(url)

    # If page type is HTML get the content
    html = None
    if page_type_code == PageType.HTML:
        driver.get(url)
        html = driver.page_source

        print('html')
        print(html)

def thread_worker(user_agent, queue, depth):
    worker_id = threading.current_thread().ident 

    while True:
        # Get a task from the queue; blocks until a task is available
        try:
            from_page_id, url, current_depth = queue.get(timeout=3)  # Adjust timeout as needed
        except Empty:
            break  # If queue is empty, exit the thread

        if current_depth > depth:
            queue.task_done()
            continue  # Skip processing if depth exceeded but ensure to mark the task as done

        try:
            # Logic to process a single URL
            fetch_and_process_url(url, user_agent, worker_id, depth)
        finally:
            # Mark the task as done once finished, to unblock the queue.join() call
            queue.task_done()