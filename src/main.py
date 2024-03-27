import crawler
from settings import USER_AGENT, SEED

def main():
    crawler.crawl(USER_AGENT, SEED, 5)

if __name__ == "__main__":
    main()
