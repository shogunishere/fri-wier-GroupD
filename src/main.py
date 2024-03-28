import crawler
from settings import USER_AGENT, SEED
import argparse
import time

num_threads = None 

def main():
    start_time = time.time()  # Start timing
    crawler.crawl(USER_AGENT, SEED, 5, num_threads)
    end_time = time.time()  # End timing
    duration = end_time - start_time
    print(f"Crawling with {num_threads} thread(s) took {duration:.2f} seconds.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a multi-threaded web crawler.')
    parser.add_argument('num_threads', type=int, help='Number of threads to use for crawling')
    args = parser.parse_args()
    num_threads = args.num_threads

    main()
