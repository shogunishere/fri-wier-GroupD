
from crawler import crawl
from settings import USER_AGENT, SEED
from crawler import queue

def main():
    for seed_url in SEED:
        queue(None, seed_url)

    crawl(USER_AGENT)

if __name__ == "__main__":
    main()
