"""历史数据爬虫模块（aqistudy.cn）。

包含 `AQIHistoryCrawler` 类，用于使用 Selenium/requests 获取网站中按月/按城市的历史 AQI 表格数据，
并将数据以 CSV 形式保存到 `data/raw`。
"""

from src.utils.request_utils import create_session, safe_get
from src.utils.selenium_utils import create_chrome_driver
from config.settings import START_YEAR, END_YEAR, REQUEST_INTERVAL, RAW_DATA_DIR
from src.utils.city_mapper import get_all_cities
from src.data_processing.storage import save_raw_data
import pandas as pd
from bs4 import BeautifulSoup
import time
import random
import os
from datetime import datetime
import re
from io import StringIO
import traceback

class AQIHistoryCrawler:
    def __init__(self):
        self.session = create_session()
        self.base_url = "https://www.aqistudy.cn/historydata/daydata.php"
        self.cities = get_all_cities()  # 获取所有城市（中文名+拼音）
        # 初始化Selenium驱动
        self.driver = create_chrome_driver()
        # 预获取所有可用日期（首次运行时执行）
        self.available_dates = self._fetch_available_dates()

    def _fetch_available_dates(self):
        """获取网站支持的日期范围列表"""
        sample_city = self.cities.get("直辖市", [])[0] if self.cities else None
        if not sample_city:
            return []
        sample_url = f"{self.base_url}?city={sample_city['pinyin']}"
        dates = []
        try:
            self.driver.get(sample_url)
            time.sleep(2)  # 等待页面加载
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            dates_ = soup.find_all('li')
            for i in dates_:
                if i.a:  # 去除空值
                    li = i.a.text  # 提取li标签下的a标签
                    date = re.findall('[0-9]*', li)  # ['2019', '', '12', '', '']
                    year = date[0]
                    month = date[2]
                    if month and year:  # 去除不符合要求的内容
                        date_new = '-'.join([year, month])
                        dates.append(date_new)
            # 去重并排序，避免重复爬取
            return sorted(list(set(dates)))
        except Exception as e:
            print(f'日期获取失败：{str(e)}')
            traceback.print_exc()
        return dates

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
        """使用Selenium爬取单个城市单个月份的每日AQI数据"""
        max_retries = 5
        retry_count = 0
        while retry_count < max_retries:
            try:
                url = f"{self.base_url}?city={city_pinyin}&month={month}"
                print(f"访问URL: {url}")
                self.driver.get(url)

                time.sleep(2 + random.uniform(0.5, 1.5))  # 随机等待时间
                
                # 解析表格数据
                html_string = StringIO(self.driver.page_source)
                tables = pd.read_html(html_string, header=0)
                
                # 模拟浏览器滚动（增强真实性）
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(1, 2))  # 滚动后等待
                
                if not tables or tables[0].empty:
                    print(f"{city_name}{month}无有效数据")
                    return None

                df = tables[0]
                # 数据清洗
                valid_cols = [col for col in ['日期', 'AQI'] if col in df.columns]
                if valid_cols:
                    df = df.dropna(subset=valid_cols)
                # 过滤重复表头
                df = df[df['日期'] != '日期'] if '日期' in df.columns else df
                
                # 添加城市和年月信息
                df["城市"] = city_name
                df["年份"] = month.split('-')[0]
                df["月份"] = month.split('-')[1]
                
                # 转换数值列
                numeric_cols = ["AQI", "PM2.5", "PM10", "SO₂", "NO₂", "CO", "O₃", "排名", "O3_8h", "SO2"]
                for col in numeric_cols:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col].replace("-", None), errors="coerce")
                
                return df if not df.empty else None
                
            except Exception as e:
                retry_count += 1
                print(f"{city_name}{month}爬取失败（第{retry_count}次重试）：{str(e)}")
                # 失败后刷新页面并更换User-Agent
                if retry_count % 2 == 0:
                    self.driver.quit()
                    self.driver = create_chrome_driver()  # 重建驱动
                time.sleep(3)
        
        print(f"{city_name}{month}多次重试失败，跳过")
        return None


    def crawl_all(self, batch_size=None):
        """爬取所有城市所有月份数据（支持批量保存）"""
        batch_count = 0
        batch_data = []
        batch_size = batch_size or HISTORY_CRAWL_BATCH_SIZE  # 默认每X个城市保存一次
        # batch_size = batch_size or HISTORY_CRAWL_BATCH_SIZE  # 默认每X(默认10)个城市保存一次
        print(f"使用Selenium获取到可用日期: {len(self.available_dates)}个")
        
        # 筛选日期范围
        filtered_dates = [
            d for d in self.available_dates 
            if START_YEAR <= int(d.split('-')[0]) <= END_YEAR
            and int(d.replace("-", "")) <= int(datetime.now().strftime("%Y%m"))
        ]
        print(f"筛选后待爬取月份：{filtered_dates}，共{len(filtered_dates)}个")
        
        for province, city_list in self.cities.items():
            print(f"\n开始爬取{province}数据...")
            for city in city_list:
                city_name = city["name"]
                city_pinyin = city["pinyin"]
                print(f"正在爬取 {city_name}（{city_pinyin}）...")
                
                for month in filtered_dates:
                    df = self.crawl_city_month_data(city_pinyin, city_name, month)
                    if df is not None and not df.empty:
                        batch_data.append(df)
                        print(f"成功爬取{city_name}{month}数据，共{len(df)}条")
                    
                    # 月份间增加随机间隔，增强抗反爬
                    time.sleep(REQUEST_INTERVAL + float(random.uniform(0.5, 1.5)))
                
                # 城市间间隔更长一些
                time.sleep(REQUEST_INTERVAL * 2 + float(random.uniform(1, 3)))
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
        
        # 爬取完成后关闭浏览器
        self.driver.quit()
        print("\n🔌 浏览器已关闭")

    def _save_batch(self, batch_data):
        """批量保存数据到CSV"""
        if not batch_data:
            return
        combined_df = pd.concat(batch_data, ignore_index=True)
        # 按年份+城市分组保存（每个城市每年一个文件）
        for (year, city), df in combined_df.groupby(["年份", "城市"]):
            filename = f"{year}_{city}_aqi_history.csv"
            file_path = os.path.join(RAW_DATA_DIR, filename)
            # 追加模式，避免重复爬取时覆盖已存在数据
            df.to_csv(
                file_path,
                mode='a' if os.path.exists(file_path) else 'w',
                header=not os.path.exists(file_path),
                index=False,
                encoding="utf-8-sig"
            )
        print(f"批量保存完成✅，共{len(combined_df)}条数据")

if __name__ == "__main__":
    from config.settings import HISTORY_CRAWL_BATCH_SIZE
    crawler = AQIHistoryCrawler()
    crawler.crawl_all(batch_size=HISTORY_CRAWL_BATCH_SIZE)