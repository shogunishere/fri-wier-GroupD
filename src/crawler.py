
from datetime import datetime
from collections import deque

from driver import get_driver
from database import get_site, get_page, insert_site, insert_page, insert_link, insert_binary, insert_image
from utils import get_domain, get_base_url, get_url_path, get_http_headers, get_urls, fetch_images, fetch_robots_txt, fetch_sitemap
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

        # Get http headers with a new request
        status_code, page_type_code = get_http_headers(url)

        # Process site
        base_url = get_base_url(url)
        site_id = process_site(base_url)
        
        # Process page
        path_url = get_url_path(url)
        page_id = process_page(path_url, site_id, status_code, page_type_code, html, accessed_time)
        
        # Continue only if page is not yet saved in the database
        if page_id is not None: 
            # Link if not the seed
            if (from_page_id): insert_link(from_page_id, page_id)

            # Process images
            imgs = fetch_images(html, base_url)
            for filename, content_type, data in imgs:
                process_image(page_id, filename, content_type, data, accessed_time)

            # Add to queue newly found URLs
            new_urls = get_urls(html, url)
            for new_url in new_urls:
                queue.append((page_id, new_url, current_depth + 1))

    driver.quit()

def process_site(base_url):
    robots_txt = fetch_robots_txt(base_url)
    sitemap = fetch_sitemap(base_url)

    domain = get_domain(base_url)

    site_id = get_site(domain)

    if (site_id is None):
        site_id = insert_site(domain, robots_txt, sitemap)
        print(f"New site [id: {site_id}]")
    else:
        print(f"Existing site [id: {site_id}]")

    return site_id

def process_page(url, site_id, status_code, page_type_code, html, accessed_time):

    # TODO: check hash

    page_id = get_page(url)

    if (page_id is None):
        page_id = insert_page(site_id, page_type_code, url, html, status_code, accessed_time)
        print(f"New page [id: {page_id}]")
        
        # if (page_type_code == PageType.HTML):
        #     page_id = insert_page(site_id, page_type_code, url, html, status_code, accessed_time)
        #     print(f"New page [id: {page_id}]")

        # if (page_type_code == PageType.BINARY):
        #     binary_id = insert_binary(page_id, 1, 1)
        #     print(f"New binary [id: {binary_id}]")

        return page_id
    else:
        print(f"Existing page [id: {page_id}]")
        return None

def process_image(page_id, filename, content_type, data, accessed_time):
    image_id = insert_image(page_id, filename, content_type, data, accessed_time)
    print(f"New image [filename: {filename}]")
