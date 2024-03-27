import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
import xml.etree.ElementTree as ET
from io import StringIO

from models import PageType

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


def get_url_path(url):
    parsed_url = urlparse(url)
    return parsed_url.path

def fetch_http_headers(url):
    try:
        response = requests.head(url)
        content_type = response.headers.get('Content-Type', 'text/html')
        page_type_code = PageType.HTML
        if 'text/html' in content_type:
            page_type_code = PageType.HTML
        elif 'application/pdf' in content_type:
            page_type_code = PageType.BINARY

        return response.status_code, page_type_code
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None, None
    
def get_urls(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for link in soup.find_all('a', href=True):
        full_url = urljoin(base_url, link['href'])
        urls.append(full_url)
    return urls

def fetch_images(html, base_url):
    imgs = []
    soup = BeautifulSoup(html, 'html.parser')
    for img in soup.find_all('img'):
        img_url = urljoin(base_url, img.get('src'))
        if img_url:
            try:
                response = requests.get(img_url)
                if response.status_code == 200:
                    content_type = response.headers['content-type']
                    data = response.content
                    filename = img_url.split('/')[-1]
                    imgs.append((filename, content_type, data))
            except requests.RequestException as e:
                print(f"Error fetching image from {img_url}: {e}")

    return imgs

def fetch_robots_txt(base_url):
    url = f"{base_url}/robots.txt"
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching robots.txt from {url}: {e}")
        return None

def fetch_sitemap(base_url, sitemap_location=None):
    url = sitemap_location or f"{base_url}/sitemap.xml"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching sitemap from {url}: {e}")
        return None
    
def parse_robots_txt(robots_txt, user_agent):
    
    rules = {"Allow": [], "Disallow": [], "Crawl-delay": None, "Sitemap": None}
    user_agent_specific = False

    if robots_txt is None:
        return rules
 
    for line in robots_txt.split("\n"):
        line = line.strip()

        if not line or line.startswith("#"):  
            continue

        # Split the line into key and value using robust method
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

def parse_sitemap(sitemap):
    urls = []

    # Handling potential encoding declaration issues
    try:
        # If the sitemap content is a byte string, decode it
        if isinstance(sitemap, bytes):
            sitemap = sitemap.sitemap('utf-8')

        # Parse the XML content
        tree = ET.parse(StringIO(sitemap))
        root = tree.getroot()

        # Namespace handling (if the sitemap XML uses namespaces)
        namespaces = {'ns': root.tag.split('}')[0].strip('{')}

        # Extracting URLs
        for url in root.findall('ns:url/ns:loc', namespaces=namespaces):
            urls.append(url.text)

    except ET.ParseError as e:
        print(f"Error parsing sitemap XML: {e}")

    return urls

def is_url_allowed(url, rules):
    if not rules or ('Allow' in rules and not rules['Allow']):
        return True  # Allow all if no explicit rules

    parsed_url = urlparse(url)
    for disallowed_path in rules.get('Disallow', []):
        if parsed_url.path.startswith(disallowed_path):
            return False

    return True

def remove_null_characters(content):
    return content.replace('\x00', '') if content else content