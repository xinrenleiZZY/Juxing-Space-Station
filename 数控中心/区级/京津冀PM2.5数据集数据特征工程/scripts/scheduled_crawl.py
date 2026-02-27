import time
from scripts.run_realtime_crawl import *

if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception:
            pass
        time.sleep(3600)
