
from crawler import crawl_worker
from settings import USER_AGENT, SEED, WORKERS
from crawler import bulk_queue
import threading


def main():
    bulk_queue(None, SEED)

    threads = []
    for i in range(WORKERS):
        worker_name = f"W{i}"
        thread = threading.Thread(target=crawl_worker, name=worker_name, args=(USER_AGENT, worker_name))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
