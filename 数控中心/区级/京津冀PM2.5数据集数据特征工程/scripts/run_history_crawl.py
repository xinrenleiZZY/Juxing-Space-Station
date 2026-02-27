# scripts/run_history_crawl.py
import os
import sys

# 将项目根目录添加到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.crawlers.aqi_history import AQIHistoryCrawler
from config.settings import HISTORY_CRAWL_BATCH_SIZE

if __name__ == '__main__':
    crawler = AQIHistoryCrawler()
    crawler.crawl_all(batch_size=HISTORY_CRAWL_BATCH_SIZE)
