from src.utils.request_utils import create_session, safe_post, get_headers
from config.settings import NEWRAW_DATA_DIR, SAVE_TO_SQLITE
from src.utils.city_mapper import get_city_code_map
from src.data_processing.storage import save_raw_data, save_to_sqlite
import pandas as pd
import time
from datetime import datetime
import os
import re
import logging
import random
import requests  # 直接引入requests处理POST请求

# 配置日志输出
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('aqi_realtime_crawl.log', encoding='utf-8')  # 新增文件日志
    ]
)

class AQIRealtimeCrawler:
    def __init__(self):
        self.session = create_session()
        # 基础API URL（通过citycode区分城市）
        self.base_api = "https://air.cnemc.cn:18007/HourChangesPublish/GetCityRealTimeAqiHistoryByCondition"
        # 城市编码映射
        self.city_codes = get_city_code_map()
        # 记录总进度
        self.total_cities = len(self.city_codes)
        self.completed_cities = 0
        
    def _get_headers(self):
        """生成符合接口要求的请求头"""
        return get_headers(referer="https://air.cnemc.cn:18007/")  # 传入实时接口的 Referer
    
    def _parse_timepoint(self, timepoint_str):
        """解析TimePointStr格式为日期和小时（增强容错）"""
        if not timepoint_str:
            return None, None
            
        # 匹配格式如"02日20时"
        match = re.match(r"(\d{2})日(\d{2})时", timepoint_str)
        if match:
            day, hour = match.groups()
            # 获取当前年月
            now = datetime.now()
            current_year, current_month = now.year, now.month
            
            # 处理跨月情况（如本月1日爬取上月31日数据）
            try:
                datetime(current_year, current_month, int(day))
            except ValueError:
                current_month -= 1
                if current_month == 0:
                    current_month = 12
                    current_year -= 1
            
            date_str = f"{current_year}-{current_month:02d}-{day}"
            return date_str, hour
        return None, None
    
    def crawl_city_realtime(self, city_name):
        """爬取单个城市的实时AQI数据（按小时）"""
        logging.info(f"🚀 开始处理城市: {city_name}")
        
        city_code = self.city_codes.get(city_name)
        if not city_code:
            logging.error(f"⚠️ 未找到{city_name}的城市编码，跳过该城市")
            return None

        # 构造请求参数
        params = {
            "citycode": city_code,
            "_": int(time.time() * 1000)  # 时间戳防缓存
        }

        # 发送POST请求（关键修改）
        logging.info(f"🚦向API发送POST请求获取🌍 {city_name}数据...")
        response = safe_post(
            self.session,
            self.base_api,
            params=params,
            referer="https://air.cnemc.cn:18007/",  # 传入实时接口的referer
            timeout=15
        )

        if not response:
            logging.error(f"❌ {city_name}请求失败，未获取到响应")
            return None

        try:
            # 解析JSON数据
            data = response.json()
            # 处理可能的外层包装（部分接口返回格式可能包含data字段）
            if isinstance(data, dict) and "data" in data:
                data = data["data"]
                
            logging.info(f"✅ 成功获取{city_name}原始数据，共{len(data)}条时间点记录 📋")
            
            all_hour_data = []
            for idx, item in enumerate(data):
                # 解析时间点
                date_str, hour = self._parse_timepoint(item.get("TimePointStr", ""))
                if not date_str or not hour:
                    logging.warning(f"⏳ 跳过无效时间格式记录: {item.get('TimePointStr')}")
                    continue
                    
                # 统一处理空值和特殊符号
                def parse_numeric(value):
                    if value in ["—", "", "None", None]:
                        return None
                    try:
                        return float(value)
                    except ValueError:
                        return None

                hour_data = {
                    "城市": city_name,
                    "日期": date_str,
                    "小时": hour,
                    "AQI": parse_numeric(item.get("AQI")),
                    "空气质量等级": item.get("Quality", "").strip(),
                    "PM2.5": parse_numeric(item.get("PM2_5")),
                    "PM10": parse_numeric(item.get("PM10")),
                    "SO₂": parse_numeric(item.get("SO2")),
                    "NO₂": parse_numeric(item.get("NO2")),
                    "CO": parse_numeric(item.get("CO")),
                    "O₃": parse_numeric(item.get("O3")),
                    "首要污染物": item.get("PrimaryPollutant", "").replace("—", "").strip(),
                    "健康建议": item.get("Unheathful", "").strip(),
                    "措施建议": item.get("Measure", "").strip(),
                    "采集时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                all_hour_data.append(hour_data)
                
                # 每解析10条数据显示一次进度
                if (idx + 1) % 10 == 0:
                    logging.info(f" ├─⏳ {city_name}数据解析进度: {idx + 1}/{len(data)}")

            df = pd.DataFrame(all_hour_data)
            logging.info(f" └─🎯 {city_name}数据解析完成，共{len(df)}条有效记录")
            return df

        except Exception as e:
            logging.error(f" └─ ❌ 解析{city_name}数据失败: {str(e)}", exc_info=True)
            return None

    def crawl_realtime_batch(self, cities=None):
        """批量爬取多个城市的实时数据"""
        cities = cities or list(self.city_codes.keys())
        all_realtime_data = []
        
        start_time = datetime.now()
        logging.info(f"=============== 开始爬取京津冀实时AQI数据 ===============")
        logging.info(f"⏱️ 爬取时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logging.info(f"🧩 待爬取城市数量: {len(cities)}")
        logging.info(f"🗺️ 城市列表: {', '.join(cities)}")
        
        for i, city in enumerate(cities, 1):
            logging.info(f"\n=============== 处理第{i}/{len(cities)}个城市: {city} ===============")
            df = self.crawl_city_realtime(city)
            
            if df is not None and not df.empty:
                all_realtime_data.append(df)
                logging.info(f"✅ {city}爬取成功，获取{len(df)}条记录 📋")
            else:
                logging.warning(f"❌ {city}爬取失败或无有效数据")
                
            self.completed_cities = i
            # 显示总体进度
            progress = (self.completed_cities / self.total_cities) * 100
            logging.info(f"⏳ 当前总体进度: {progress:.1f}% ({self.completed_cities}/{self.total_cities})")
            
            if i < len(cities):
                wait_time = random.uniform(1.5, 3.5)  # 随机等待时间，避免反爬
                logging.info(f"🔄 等待{wait_time:.1f}秒后继续下一个城市...")
                time.sleep(wait_time)
        
        if all_realtime_data:
            combined = pd.concat(all_realtime_data, ignore_index=True)
            # 确保存储目录存在
            os.makedirs(NEWRAW_DATA_DIR, exist_ok=True)
            # 按时间戳保存
            filename = f"realtime_京津冀_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
            file_path = os.path.join(NEWRAW_DATA_DIR, filename)
            # 使用统一保存函数：写入 CSV（NEWRAW_DATA_DIR 的绝对路径）并根据配置写入 SQLite
            try:
                if SAVE_TO_SQLITE:
                    save_raw_data(combined, filename=file_path, table_name='realtime_data')
                else:
                    # 仅保存 CSV
                    combined.to_csv(file_path, index=False, encoding="utf-8-sig")
                logging.info("📄 realtime 数据保存完成。")
            except Exception as e:
                logging.error(f"⚠️ 保存 realtime 数据失败：{e}")
            
            end_time = datetime.now()
            elapsed = (end_time - start_time).total_seconds()
            logging.info(f"\n=============== 爬取完成 ===============")
            logging.info(f"⏱️ 总耗时: {elapsed:.2f}秒")
            logging.info(f"📁 保存文件路径: {file_path}")
            logging.info(f"📌 总记录数: {len(combined)}条")
            logging.info(f"📍 平均每个城市: {len(combined)/len(cities):.1f}条记录")
            logging.info(f">>>✅ realtime数据爬取与保存成功！>>>")
            return combined
        else:
            end_time = datetime.now()
            elapsed = (end_time - start_time).total_seconds()
            logging.warning(f"\n===== 爬取完成但未获取到任何有效数据 =====")
            logging.info(f"⏱️ 总耗时: {elapsed:.2f}秒")
            return None

if __name__ == "__main__":
    logging.info("🚀 启动京津冀实时AQI数据爬虫...")
    try:
        crawler = AQIRealtimeCrawler()
        result = crawler.crawl_realtime_batch()
    except Exception as e:
        logging.critical(f"❌ 爬虫运行失败: {str(e)}", exc_info=True)
    finally:
        logging.info("✅ 爬虫执行结束")