
from crawler import crawl
from settings import USER_AGENT, SEED
from crawler import bulk_queue

def main():
    bulk_queue(None, SEED)

    crawl(USER_AGENT)

if __name__ == "__main__":
    main()
