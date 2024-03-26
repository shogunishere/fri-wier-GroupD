import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse

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

def get_http_headers(url):
    try:
        response = requests.get(url)
        content_type = response.headers['Content-Type']
        
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