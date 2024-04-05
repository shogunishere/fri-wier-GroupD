import requests
from bs4 import BeautifulSoup, UnicodeDammit
from urllib.parse import urljoin
from urllib.parse import urlparse
import xml.etree.ElementTree as ET
from io import StringIO
from time import sleep
from datetime import datetime
from hashlib import sha256

from settings import TIMEOUT

from models import PageType, BinaryType

# Without https://
def get_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    if domain.startswith('www.'):
        domain = domain[4:] 

    return domain


# With https://
def get_base_url(url):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    return base_url


# Path with parameters
def get_url_path(url):
    parsed_url = urlparse(url)
    path = parsed_url.path if parsed_url.path else "/"
    if parsed_url.query:
        path += "?" + parsed_url.query
    return path


# Fetch status code and content type with head request
def fetch_http_headers(url):
    try:
        response = requests.head(url)
        content_type = response.headers.get('Content-Type', 'text/html')
        page_type_code = PageType.HTML
        print(f"Response is: {response.headers}")
        print(f"Content type is {content_type}")
        content_type_mapping = {
            'text/html': PageType.HTML,
            'application/pdf': BinaryType.PDF,
            'application/vnd.ms-powerpoint': BinaryType.PPT,
            'application/vnd.openxmlformats-officedocument.presentationml.presentation': BinaryType.PPTX,
            'application/msword': BinaryType.DOC,
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': BinaryType.DOCX
        }

        for key, value in content_type_mapping.items():
            if key in content_type:
                page_type_code = value
                break

        return response.status_code, page_type_code
    except requests.RequestException as e:
        return None, None


# Get all urls from the HTML
def get_urls(html, base_url):
    dammit = UnicodeDammit(html)
    html = dammit.unicode_markup
    soup = BeautifulSoup(html, 'html.parser')

    urls = []
    for link in soup.find_all('a', href=True):
        full_url = urljoin(base_url, link['href'])
 
        parsed_url = urlparse(full_url)
        if parsed_url.scheme == 'https' and parsed_url.netloc:
            urls.append(full_url)
    return urls


# Get all images from the HTML
def fetch_images(html, base_url):
    imgs = []
    soup = BeautifulSoup(html, 'html.parser')
    for img in soup.find_all('img'):
        img_url = urljoin(base_url, img.get('src'))
        if img_url:
            try:
                response = requests.get(img_url)
                if response.status_code == 200:
                    content_type = response.headers.get('content-type')
                    if content_type:
                        data = response.content
                        filename = img_url.split('/')[-1]
                        imgs.append((filename, content_type, data))
            except requests.RequestException as e:
                # print(f"[Error] Error fetching image from {img_url}: {e}")
                pass

    return imgs


# Fetch robots.txt from the site
def fetch_robots_txt(base_url):
    url = f"{base_url}/robots.txt"
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return response.text
    except requests.RequestException as e:
        return None


# Fetch sitemap from the site
def fetch_sitemap(url):
    if url is None:
        return None
    try:
        response = requests.get(url, timeout=1)
        response.raise_for_status() 
        return response.content.decode('utf-8')
    except Exception as e:
        return None
    

# Parse robots.txt do dictionary
def parse_robots_txt(robots_txt, user_agent):
    rules = {"Allow": [], "Disallow": [], "Crawl-delay": TIMEOUT, "Sitemap": None}
    user_agent_specific = False

    if robots_txt is None:
        return rules
 
    for line in robots_txt.split("\n"):
        line = line.strip()

        if not line or line.startswith("#"):  
            continue

        parts = line.split(":", 1)
        if len(parts) != 2:
            continue  # Invalid line

        key = parts[0].strip().lower()
        value = parts[1].strip()

        if key == "user-agent": 
            if value == '*' or value.lower() == user_agent.lower():
                user_agent_specific = True
            else:
                user_agent_specific = False
        elif key == "sitemap":
            rules["Sitemap"] = value
        elif user_agent_specific:
            if key in ["allow", "disallow"]:
                rules[key.capitalize()].append(value)
            elif key == "crawl-delay":
                rules["Crawl-delay"] = int(value)


    return rules


# Parse sitemap recursively to avoid links to other sitemaps
def parse_sitemap_recursively(sitemap, urls=[], root_url=None, max_urls=25):
    try:    
        if isinstance(sitemap, bytes):
            sitemap = sitemap.decode('utf-8')

        tree = ET.parse(StringIO(sitemap))
        root = tree.getroot()

        namespaces = {'ns': root.tag.split('}')[0].strip('{')}

        if root.tag.endswith('}sitemapindex'):
            # Process sitemap index
            for sitemap_elem in root.findall('ns:sitemap/ns:loc', namespaces=namespaces):
                if len(urls) >= max_urls:
                    return urls  # Early return if max_urls reached
                sitemap_url = sitemap_elem.text
                nested_sitemap_content = fetch_sitemap(sitemap_url)
                if nested_sitemap_content:
                    urls = parse_sitemap_recursively(nested_sitemap_content, urls, sitemap_url, max_urls)
        else:
            # Process regular sitemap
            for url_elem in root.findall('ns:url/ns:loc', namespaces=namespaces):
                if len(urls) >= max_urls:
                    return urls  # Early return if max_urls reached
                urls.append(url_elem.text)

    except ET.ParseError as e:
        print(f"[Error] Error parsing sitemap XML: {e}")
        if root_url:
            print(f"[Info] The problematic sitemap was at: {root_url}")

    return urls



# From robots.txt check if url is allowed
def is_url_allowed(url, rules):
    if not rules or ('Allow' in rules and not rules['Allow']):
        return True  # Allow all if no explicit rules

    parsed_url = urlparse(url)
    for disallowed_path in rules.get('Disallow', []):
        if parsed_url.path.startswith(disallowed_path):
            return False

    return True


# Make sure sitemap content doesn't contain null characters when inserting in database
def remove_null_characters(content):
    return content.replace('\x00', '') if content else content


# Sleep the thread to reach site's timeout
def wait(current_time, last_access_time, timeout):
    if last_access_time is None:
        return None
    
    time_delta = current_time - last_access_time

    if time_delta.total_seconds() < timeout:
        sleep_time = timeout - time_delta.total_seconds()
        print(f"[Sleeping] {sleep_time} s")
        sleep(sleep_time)


# Generate SHA256 hash
def generate_hash(content):
    return sha256(content.encode('utf-8')).hexdigest()
    
