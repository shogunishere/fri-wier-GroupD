
from datetime import datetime
from selenium.common.exceptions import WebDriverException

from driver import get_driver
from database import get_site, get_page_by_url, get_rules, get_last_accessed_time, start_frontier, get_duplicate_html, insert_site, insert_frontier, insert_link, insert_binary, insert_image, update_page, update_site_time, finish_frontier
from utils import get_domain, get_base_url, get_url_path, fetch_http_headers, get_urls, fetch_images, fetch_robots_txt, fetch_sitemap, parse_robots_txt, parse_sitemap_recursively, is_url_allowed, wait, generate_hash
from models import PageType


def crawl(user_agent):
    driver = get_driver()

    while True:

        frontier_id, frontier_url = start_frontier()

        if frontier_id is None:
            print("Frontier is empty! Exiting.")
            break
        
        current_time = datetime.now()

        print("-" * 75)
        print(f"[Retrieving] {frontier_url}:")

        status_code, page_type_code = fetch_http_headers(frontier_url)
       
        if status_code is None and page_type_code is None:
            finish_frontier(frontier_id, PageType.FAIL, status_code)
            print(f"[Fail] Continuing with next frontier. Page down.")
            continue

        site_id, site_rules, sitemap_urls, site_last_access_time = process_site(frontier_url, user_agent)

        if not is_url_allowed(frontier_url, site_rules):
            finish_frontier(frontier_id, PageType.DISALLOWED, status_code)
            print(f"[Disallowed] Continuing with next frontier. Page disallowed by robots.txt.")
            continue
    
        for sitemap_url in sitemap_urls:
            queue(frontier_id, sitemap_url)

        update_site_time(site_id, current_time)

        timeout = site_rules.get("Crawl-delay") if site_rules else 0

        wait(current_time, site_last_access_time, timeout)

        if page_type_code == PageType.HTML:
            try:
                driver.get(frontier_url)
                html = driver.page_source
            except WebDriverException as e:
                finish_frontier(frontier_id, PageType.FAIL, status_code)
                print(f"[Error] Continuing with next frontier. Driver error: {e}")
                continue

            new_urls = process_html(frontier_id, site_id, frontier_url, html, status_code, current_time)

            for new_url in new_urls:
                if is_url_allowed(new_url, site_rules):
                    queue(frontier_id, new_url)

        elif page_type_code == PageType.BINARY:
            process_binary(frontier_id, site_id, frontier_url, status_code, current_time)

        finish_frontier(frontier_id, None, status_code)
        print(f"[Finish] Successfully processed the page (id: {frontier_id}).")


    driver.quit()


def queue(from_page_id, url):
    current_time = datetime.now()

    page_exists = get_page_by_url(url)

    if not page_exists:
        page_id = insert_frontier(url, current_time)
        insert_link(from_page_id, page_id)
        print(f"[Frontier] Added {url}")

    else:
        print(f"[Frontier] Already exists {url}")
    

def process_site(url, user_agent):
    base_url = get_base_url(url)
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
            sitemap = fetch_sitemap(rules["Sitemap"])
            if sitemap:
                sitemap_urls = parse_sitemap_recursively(sitemap)

        site_id = insert_site(domain, robots_txt, sitemap)

        print(f"[Site] Site not found. Created new.")
        print(f"[Robots] Robots.txt {'found' if robots_txt else 'not found'}.")
        print(f"[Sitemap] Found {len(sitemap_urls)} URLs in sitemap.")

        return site_id, rules, sitemap_urls, None

    else:
        robots_txt = get_rules(site_id)
        rules = parse_robots_txt(robots_txt, user_agent)
        last_access_time = get_last_accessed_time(site_id)

        print(f"[Site] Site already exists. Found it.")

        return site_id, rules, [], last_access_time


def process_html(frontier_id, site_id, url, html, status_code, current_time):
    path_url = get_url_path(url)
    base_url = get_base_url(url)

    html_hash = generate_hash(html)
    if get_duplicate_html(html_hash):
        update_page(frontier_id, site_id, path_url, PageType.DUPLICATE, None, html_hash, status_code, current_time)
        print(f"[Duplicate] Page updated as DUPLICATE.")

        return []

            
    update_page(frontier_id, site_id, path_url, PageType.HTML, html, html_hash, status_code, current_time)

    # Process html images
    imgs = fetch_images(html, base_url)
    for filename, content_type, data in imgs:
        process_image(frontier_id, filename, content_type, data, current_time)

    # Get html urls
    new_urls = get_urls(html, base_url)

    print(f"[HTML] Page updated as HTML.")
    print(f"[Images] Found {len(imgs)} images. Added them.")

    return new_urls 


def process_binary(frontier_id, site_id, url, status_code, current_time):
    path_url = get_url_path(url)

    update_page(frontier_id, site_id, path_url, PageType.BINARY, None, None, status_code, current_time)
    insert_binary(frontier_id, None, None) # Not adding binary data

    print(f"[Binary] Page updated as BINARY.")


def process_image(page_id, filename, content_type, data, current_time):
    image_id = insert_image(page_id, filename, content_type, data, current_time)
