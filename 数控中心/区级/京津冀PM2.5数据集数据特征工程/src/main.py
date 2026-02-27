"""项目主程序入口。

提供最小的命令行入口，用于触发历史数据或实时数据抓取。该模块仅用于开发与调试，
生产部署应使用更成熟的任务调度/运行方式。
"""

import sys
import time
from typing import Optional
import os
import runpy


def run_history(batch_size: Optional[int] = None):
	"""运行历史数据爬取（调用 `src.crawlers.aqi_history.AQIHistoryCrawler`）。"""
	try:
		from src.crawlers.aqi_history import AQIHistoryCrawler
		from config.settings import HISTORY_CRAWL_BATCH_SIZE
	except Exception as e:
		print(f"无法导入历史爬虫模块：{e}")
		return

	crawler = AQIHistoryCrawler()
	crawler.crawl_all(batch_size=batch_size or HISTORY_CRAWL_BATCH_SIZE)


def run_realtime(cities: Optional[list] = None):
    """运行实时数据爬取（调用 `src.crawlers.aqi_realtime.AQIRealtimeCrawler`）。"""
    try:
        from src.crawlers.aqi_realtime import AQIRealtimeCrawler
    except Exception as e:
        print(f"无法导入实时爬虫模块：{e}")
        return

    crawler = AQIRealtimeCrawler()
    crawler.crawl_realtime_batch(cities=cities)


# 导入定时实时爬取功能
from src.crawlers.scheduled_realtime import run_scheduled_realtime


def query_sqlite():
    """把后续 CLI 参数转发给 `scripts/query_db.py` 并以脚本方式运行。"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    script_path = os.path.join(project_root, "scripts", "query_db.py")
    # set sys.argv for the script (drop the 'src.main' and 'query' parts)
    old_argv = sys.argv[:]
    try:
        sys.argv = [old_argv[0]] + old_argv[2:]
        runpy.run_path(script_path, run_name="__main__")
    finally:
        sys.argv = old_argv


def run_sync_csv_to_db():
    """把后续 CLI 参数转发给 `scripts/sync_csv_to_db.py` 并以脚本方式运行（支持 dry-run / real）。"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    script_path = os.path.join(project_root, "scripts", "sync_csv_to_db.py")
    old_argv = sys.argv[:]
    try:
        sys.argv = [old_argv[0]] + old_argv[2:]
        runpy.run_path(script_path, run_name="__main__")
    finally:
        sys.argv = old_argv

# 导入数据清洗功能
from src.data_processing.cleaner_manager import run_clean_history, run_clean_realtime, run_clean


# 导入数据同步功能
from src.data_processing.data_sync import data_sync


def _usage():
    print("✅ 欢迎使用-AQI数据采集项目！🎯")
    print("🔄 用法: python -m src.main [history|realtime|history_realtime|scheduled|query|sync|clean_history|clean_realtime|clean|data_sync]")
    print("  ├─ history:    🚀 运行历史数据爬取")
    print("  ├─ realtime:   🚀 运行单次实时数据爬取")
    print("  ├─ history_realtime:   🚀 同时运行 历史数据 和 实时数据爬取")
    print("  ├─ scheduled:  🛑 启动定时任务，每小时运行一次实时爬取")
    print("  ├─ query:      🔎 启动交互式数据库查看器（REPL）或执行查询，例如：")
    print("                  ├─ python -m src.main query --list")
    print("                  ├─ python -m src.main query --info raw_data")
    print("                  └─ python -m src.main query (进入交互模式)")
    print("  ├─ sync:       🔁 将 data 中的 CSV 同步到数据库（历史/实时）。用法示例：") 
    print("                  ├─ python -m src.main sync --target both")
    print("                  └─ python -m src.main sync --target realtime --dry-run")
    print("  ├─ clean_history:  🧹 清洗历史数据（扫描 data/Hisraw 并保存 processed/ + DB）")
    print("  ├─ clean_realtime: 🧹 清洗实时数据（扫描 data/Newraw 并保存 processed/ + DB）")
    print("  ├─ clean:          🧹 同时清洗历史与实时数据（先历史后实时）")
    print("  └─ data_sync:      🔄 同步processed的CSV文件到lstm_analysis/data_preparation")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        _usage()
        sys.exit(1)

    cmd = sys.argv[1].lower()
    if cmd == "history":
        run_history()
    elif cmd == "realtime":
        run_realtime()
    elif cmd == "history_realtime":
        # 同时爬取历史和实时
        run_history()
        run_realtime()
    elif cmd == "scheduled":
        run_scheduled_realtime()  # 新增定时任务命令
    elif cmd == "query":
        query_sqlite()
    elif cmd == "sync":
        # 将后续参数传递给 scripts/sync_csv_to_db.py，并以脚本形式运行（dry-run / real run）
        run_sync_csv_to_db()
    elif cmd == "clean_history":
        # 清洗历史数据（data/raw）
        run_clean_history()
    elif cmd == "clean_realtime":
        # 清洗实时数据（data/Newraw）
        run_clean_realtime()
    elif cmd == "clean":
        run_clean()
    elif cmd == "data_sync":
        data_sync()
    else:
        _usage()
