import crawler
from settings import SEED

def main():
    seed_urls = SEED
    crawler.crawl(seed_urls, 5)

if __name__ == "__main__":
    main()
