
from datetime import datetime
from collections import deque

from driver import get_driver
from database import get_site, get_page, get_rules, insert_site, insert_page, insert_link, insert_binary, insert_image
from utils import get_domain, get_base_url, get_url_path, fetch_http_headers, get_urls, fetch_images, fetch_robots_txt, fetch_sitemap, parse_robots_txt, parse_sitemap, is_url_allowed
from models import PageType

def crawl(user_agent, seed_urls, depth):
    driver = get_driver()

    queue = deque([(None, url, 1) for url in seed_urls]) # Double ended queue (FIFO) (From page id, current url, current depth)

    while queue:
        from_page_id, url, current_depth = queue.popleft()  
        if current_depth > depth:
            break # Break out if maximum depth is exceeded

        # Start retrieving
        print(f"Retrieving page URL '{url}' at depth {current_depth}")
        accessed_time = datetime.now()

        # Make http head request
        status_code, page_type_code = fetch_http_headers(url)
        
        # If page type is HTML get the content
        html = None
        if page_type_code == PageType.HTML:
            driver.get(url)
            html = driver.page_source

        # Process site
        base_url = get_base_url(url)
        site_id, rules, sitemap_urls = process_site(base_url, user_agent)

        if not is_url_allowed(url, rules):
            print(f"URL '{url}' is disallowed by robots.txt")
            continue
        
        # Process page
        path_url = get_url_path(url)
        page_id = process_page(path_url, site_id, status_code, page_type_code, html, accessed_time)

        # Add sitemap urls to the queue
        for sitemap_url in sitemap_urls:
            queue.append((page_id, sitemap_url, current_depth + 1))

        # Continue only if page is not yet saved in the database
        if html is not None and page_id is not None: 
            # Save where it came from
            if (from_page_id): insert_link(from_page_id, page_id)

            # Process images
            imgs = fetch_images(html, base_url)
            for filename, content_type, data in imgs:
                process_image(page_id, filename, content_type, data, accessed_time)

            # Add to frontier (queue) newly found URLs
            new_urls = get_urls(html, url)
            for new_url in new_urls:
                if is_url_allowed(new_url, rules):
                    queue.append((page_id, new_url, current_depth + 1))

    driver.quit()

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
