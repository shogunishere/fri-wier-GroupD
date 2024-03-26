
from datetime import datetime
from collections import deque

from driver import get_driver
from database import get_site, get_page, insert_site, insert_page, insert_link
from utils import get_domain, get_base_url, get_url_path, get_http_headers, get_urls, get_image_urls, fetch_robots_txt, fetch_sitemap
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
        base_url = get_base_url(url)
        site_id = process_site(base_url)
        
        # Process page
        path_url = get_url_path(url)
        page_id = process_page(path_url, site_id, status_code, page_type_code, html, accessed_time)

        # Link if not the seed
        if (from_page_id): insert_link(from_page_id, page_id)

        # Process images
        image_urls = get_image_urls(html)
        for image_url in image_urls:
            process_image(image_url)

        # Populate queue with newly found URLs
        new_urls = get_urls(html, url)
        for new_url in new_urls:
            queue.append((page_id, new_url, current_depth + 1))

    driver.quit()

def process_site(base_url):
    robots_txt = fetch_robots_txt(base_url)
    sitemap = fetch_sitemap(base_url)

    # TODO: Check if site exists with get_site

    domain = get_domain(base_url)

    site_id = get_site(domain)

    if (site_id is None):
        site_id = insert_site(domain, robots_txt, sitemap)
        print(f"New site [id: {site_id}]")
    else:
        print(f"Existing site [id: {site_id}]")

    return site_id

def process_page(url, site_id, status_code, page_type_code, html, accessed_time):

    page_id = get_page(url)

    if (page_id is None):
        page_id = insert_page(site_id, page_type_code, url, html, status_code, accessed_time)
        print(f"New page [id: {page_id}]")
    else:
        page_id = insert_page(site_id, PageType.DUPLICATE, url, None, status_code, accessed_time)
        print(f"Existing page [id: {page_id}]")

    return page_id

def process_images(html, page_id, accessed_time):
    soup = BeautifulSoup(html, 'html.parser')
    for img in soup.find_all('img'):
        img_url = img.get('src')
        if img_url:
            process_image(page_id, img_url, accessed_time)