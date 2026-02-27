"""历史数据爬虫模块（tianqihoubao.com）。

包含 `AQIHistoryCrawler` 类，用于使用 requests requests requests 获取网站中按月/按城市的历史 AQI 表格数据，
并将数据以 CSV 形式保存到 `data/raw`。
"""

from src.utils.request_utils import create_session, safe_get
from config.settings import START_YEAR, END_YEAR, REQUEST_INTERVAL, RAW_DATA_DIR, HISTORY_CRAWL_BATCH_SIZE
from src.utils.city_mapper import get_all_cities
from src.data_processing.storage import save_raw_data, save_to_sqlite
from config.settings import SAVE_TO_SQLITE
import pandas as pd
from src.utils.get_ip import get_current_ip  # 导入IP查询工具
from bs4 import BeautifulSoup
import time
import random
import os
from datetime import datetime
import re
import logging
import traceback
import requests  # 用于获取当前IP

class AQIHistoryCrawler:
    def __init__(self):
        self.session = create_session()  # 使用requests会话
        self.base_url = "https://www.tianqihoubao.com/aqi"
        self.cities = get_all_cities()  # 获取所有城市（中文名+拼音）
        # 生成可用日期范围
        self.available_dates = self._get_months_in_range(START_YEAR, END_YEAR)
        # 初始化日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler(), logging.FileHandler('history_crawl.log', encoding='utf-8')]
        )
        self.logger = logging.getLogger(__name__)
        # 爬取统计参数
        self.total_cities = sum(len(city_list) for city_list in self.cities.values())
        self.processed_cities = 0
        self.start_time = None  # 总耗时计时起点
        self.logger = logging.getLogger(__name__)
        # 新增：初始化时检查一次IP
        initial_ip = get_current_ip()
        self.logger.info(f">>>爬虫初始化完成，📍 初始IP: {initial_ip}")

    def _get_months_in_range(self, start_year, end_year):
        """生成指定年份范围内的所有月份列表,格式YYYYMM"""
        months = []
        current_year = start_year
        current_month = 1
        end_year = end_year if datetime.now().year >= end_year else datetime.now().year
        end_month = 12 if current_year < end_year else datetime.now().month
        
        while current_year <= end_year:
            month_str = f"{current_year}{current_month:02d}"
            months.append(month_str)
            if current_year == end_year and current_month == end_month:
                break
            current_month += 1
            if current_month > 12:
                current_month = 1
                current_year += 1
        return months

    def crawl_city_month_data(self, city_pinyin, city_name, month):
        """使用requests爬取单个城市单个月份的每日AQI数据"""
        max_retries = 5
        retry_count = 0
        while retry_count < max_retries:
            try:
                url = f"{self.base_url}/{city_pinyin}-{month}.html"  # 构造访问URL
                self.logger.info("=" * 60)  # 分隔线
                self.logger.info(f"🌐 访问URL: {url}")
                
                # 记录请求前时间（用于单请求耗时计算）
                request_start = time.time()
                # 获取当前IP
                current_ip = get_current_ip()
                
                # 使用安全请求方法（带重试和随机头）
                response = safe_get(
                    self.session, 
                    url, 
                    timeout=30  # 延长超时时间
                )
                
                # 计算请求耗时
                request_time = time.time() - request_start
                self.logger.info(f"📜 当前请求IP >>> {current_ip}")
                if response:
                    # 只打印关键头信息
                    user_agent = response.request.headers.get("User-Agent", "未知")
                    self.logger.info(f"🛠️  请求头关键信息: User-Agent={user_agent}")
                if not response:
                    self.logger.warning(f"{city_name}{month}请求无响应")
                    retry_count += 1
                    time.sleep(2 **retry_count)  # 指数退避
                    continue
                self.logger.info(f"⏱️  请求耗时: {request_time:.2f}秒")
                # 解析HTML
                soup = BeautifulSoup(response.text, 'lxml')
                table = soup.find("table", class_="b")

                if not table:
                    self.logger.warning(f"{city_name}{month}未找到数据表格")
                    return None
                
                # 解析表头（处理可能的嵌套结构）
                headers = [th.text.strip() for th in table.find_all("tr")[0].find_all("td")]
                # 解析表体数据
                rows = table.find_all("tr")[1:]  # 跳过表头行
                all_daily_data = []
                
                for row in rows:
                    cols = [td.text.strip() for td in row.find_all("td")]
                    if len(cols) == len(headers):
                        daily_data = dict(zip(headers, cols))
                        daily_data["城市"] = city_name
                        daily_data["年份"] = month[:4]
                        daily_data["月份"] = month[4:]
                        all_daily_data.append(daily_data)

                if not all_daily_data:
                    self.logger.warning(f"{city_name}{month}未获取到有效数据")
                    return None

                # 转换为DataFrame并处理数据类型
                df = pd.DataFrame(all_daily_data)
                # 处理数值列（原数据中的"-"或空值转换为NaN）
                numeric_cols = [
                    "AQI指数", "当天AQI排名", "PM2.5", 
                    "PM10", "No2", "So2", "Co", "O3"
                ]
                for col in numeric_cols:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col].replace("-", None), errors="coerce")
                
                self.logger.info(f"✅ {city_name}{month}爬取成功，获取{len(df)}条记录📊")
                return df if not df.empty else None

            except Exception as e:
                retry_count += 1
                self.logger.error(f"❌ {city_name}{month}爬取失败（第{retry_count}次重试）：{str(e)}")
                traceback.print_exc()
                time.sleep(2** retry_count)  # 指数退避等待
        
        self.logger.error(f"❌ {city_name}{month}多次重试失败，跳过")
        return None

    def crawl_all(self, batch_size=None):
        """爬取所有城市所有月份数据（支持批量保存）"""
        batch_count = 0
        batch_data = []
        batch_size = batch_size or HISTORY_CRAWL_BATCH_SIZE  # 默认每X个城市保存一次
        self.start_time = time.time()  # 记录总开始时间
        self.logger.info(f"📅 可用日期数量: {len(self.available_dates)}个")
        
        # 筛选日期范围
        filtered_dates = [
            d for d in self.available_dates 
            if START_YEAR <= int(d[:4]) <= END_YEAR
            and int(d) <= int(datetime.now().strftime("%Y%m"))
        ]
        self.logger.info(f"🔍 筛选后待爬取月份：{filtered_dates}，共{len(filtered_dates)}个")
        self.logger.info(f"🔍 总待爬取城市数量：{self.total_cities}")
        
        for province, city_list in self.cities.items():
            self.logger.info("-" * 50)
            self.logger.info(f"🚀 【开始爬取 🌍 {province} 数据】")
            self.logger.info(f"📅 待爬取城市数量：{len(city_list)}个")
            self.logger.info("-" * 50)
            for idx, city in enumerate(city_list, 1):
                city_name = city["name"]
                city_pinyin = city["pinyin"]
                # 城市爬取提示
                self.logger.info(
                    f"🔍 正在爬取 [{province} 🌍 {idx}/{len(city_list)}] "
                    f"{city_name}（拼音：{city_pinyin}）"
                )
                
                # 记录单个城市爬取开始时间
                city_start = time.time()
                
                for month in filtered_dates:
                    df = self.crawl_city_month_data(city_pinyin, city_name, month)
                    if df is not None and not df.empty:
                        batch_data.append(df)
                    
                    # 月份间增加随机间隔，增强抗反爬
                    time.sleep(REQUEST_INTERVAL + random.uniform(0.5, 1.5))
                
                # 计算单个城市耗时
                city_time = time.time() - city_start
                self.processed_cities += 1
                # 计算总体进度
                progress = (self.processed_cities / self.total_cities) * 100
                # 计算总耗时
                total_time = time.time() - self.start_time
                
                self.logger.info("=" * 60)  # 分隔线
                self.logger.info(f"📊 【{city_name} 处理完成】")
                self.logger.info(f"   ├─ ⏱️ 耗时：{city_time:.2f}秒")
                self.logger.info(f"   ├─ 🎯 总体进度：{progress:.1f}%（{self.processed_cities}/{self.total_cities}）")
                self.logger.info(f"   └─ ⏱️ 累计耗时：{total_time:.2f}秒")
                self.logger.info("=" * 60)  # 分隔线

                
                # 城市间间隔更长一些
                time.sleep(REQUEST_INTERVAL * 2 + random.uniform(1, 3))
                batch_count += 1

                # 批量保存
                if batch_count >= batch_size:
                    self._save_batch(batch_data)
                    batch_data = []
                    batch_count = 0
                    # 每批完成后休息一段时间
                    time.sleep(random.uniform(5, 10))
        
        # 保存剩余数据
        if batch_data:
            self._save_batch(batch_data)
            
        # 总耗时统计
        total_elapsed = time.time() - self.start_time  # 计算总耗时
        # 爬取完成时的汇总信息
        self.logger.info(">>>GOOD>>>")
        self.logger.info("🔌 【全部爬取任务完成】")
        self.logger.info(f"   ├─ 🎯 总耗时：{total_elapsed:.2f}秒")
        self.logger.info(f"   ├─ 🌍 总处理城市数：{self.processed_cities}/{self.total_cities}")
        self.logger.info(f"   └─ 📅 完成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info(">>>END>>>" + "\n" + "=" * 90 + "\n")

    def _save_batch(self, batch_data):
        """批量保存数据到CSV"""
        if not batch_data:
            return
        combined_df = pd.concat(batch_data, ignore_index=True)
        # 按年份+城市分组保存（每个城市每年一个文件）
        for (year, city), df in combined_df.groupby(["年份", "城市"]):
            filename = f"{year}_{city}_aqi_history.csv"
            # 根据配置决定是否同时写入 SQLite
            if SAVE_TO_SQLITE:
                try:
                    save_raw_data(df, filename=filename, table_name='history_data')
                except Exception as e:
                    # 回退到本地 CSV 写入（尽可能保存数据）
                    file_path = os.path.join(RAW_DATA_DIR, filename)
                    df.to_csv(
                        file_path,
                        mode='a' if os.path.exists(file_path) else 'w',
                        header=not os.path.exists(file_path),
                        index=False,
                        encoding="utf-8-sig"
                    )
                    self.logger.error(f"📁 保存到 SQLite 失败，已回退为 CSV：{e}")
            else:
                # 仅写 CSV
                file_path = os.path.join(RAW_DATA_DIR, filename)
                df.to_csv(
                    file_path,
                    mode='a' if os.path.exists(file_path) else 'w',
                    header=not os.path.exists(file_path),
                    index=False,
                    encoding="utf-8-sig"
                )
        self.logger.info(f">>>📁 批量保存完成✅，共{len(combined_df)}条数据 💾")

if __name__ == "__main__":
    crawler = AQIHistoryCrawler()
    crawler.crawl_all(batch_size=HISTORY_CRAWL_BATCH_SIZE)