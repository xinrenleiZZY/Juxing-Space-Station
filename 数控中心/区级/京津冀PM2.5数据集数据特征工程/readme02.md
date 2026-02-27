# 全国AQI数据采集系统：历史数据+实时数据爬取项目方案
## 一、项目概述
### 1. 核心目标
- **历史数据**：从 `www.tianqihoubao.com/` 爬取全国所有城市2015年至今的每日AQI数据（含PM2.5、PM10、SO₂等关键指标）。
- **实时数据**：从 `cnemc.cn`（中国环境监测总站）爬取全国城市实时AQI播报（逐小时更新，含站点级数据）。
- 数据统一存储、去重、预处理，支持后续分析/建模使用。

### 2. 技术栈
- 核心框架：Python 3.8+
- 爬虫工具：requests（请求）、BeautifulSoup4（解析）、Selenium（动态渲染）
- 数据处理：pandas（数据清洗/合并）、numpy（数值计算）
- 存储方案：SQLite（轻量本地数据库）+ CSV（备份）
- 定时任务：schedule（定时采集）、logging（日志记录）
- 辅助工具：fake-useragent（伪装请求头）、lxml（高效解析）

### 3. 项目优势
- 双数据源互补：历史数据完整性+实时数据权威性。
- 抗反爬设计：动态请求头、请求间隔、Selenium模拟浏览器。
- 增量采集：避免重复爬取，支持断点续爬。
- 标准化输出：统一数据格式，自动处理缺失值/异常值。

## 二、完整项目结构
```
aqi-data-collection/
│
├── config/                  # 配置文件目录
│   ├── __init__.py
│   ├── cities.json          # 全国城市列表（含拼音，用于拼接URL）
│   ├── city_codes.json      # 全国城市列表（含编码，用于POST查询）
│   └── settings.py          # 全局配置（请求间隔、存储路径、日志级别等）
│
├── data/                    # 数据存储目录
│   ├── raw/                 # 原始数据（CSV格式，按年份/城市分文件）
│   ├── Newraw/              # 实时爬取原始数据（CSV格式，按爬取时间分文件）
│   ├── processed/           # 处理后的数据（合并+去重）
│   └── aqi_database.db      # SQLite数据库文件
│
├── src/                     # 核心代码目录
│   ├── __init__.py
│   ├── crawlers/            # 爬虫模块
│   │   ├── __init__.py
│   │   ├── aqi_history_隧道代理版_selenium.py   # tianqihoubao.com 历史数据爬虫，需要selenium时候开启
│   │   ├── aqi_history.py   # www.tianqihoubao.com 历史数据爬虫
│   │   └── aqi_realtime.py  # cnemc.cn 实时数据爬虫
│   │
│   ├── data_processing/     # 数据处理模块
│   │   ├── __init__.py
│   │   ├── cleaner.py       # 数据清洗（去重、缺失值填充）
│   │   ├── merger.py        # 数据合并（历史+实时）
│   │   └── storage.py       # 数据存储（CSV 为主；SQLite 支持待完善，当前尚未启用）
│   │
│   ├── utils/               # 工具函数模块
│   │   ├── __init__.py
│   │   ├── logger.py        # 日志配置
│   │   ├── request_utils.py # 请求工具（伪装、重试）
│   │   └── city_mapper.py   # 城市中文名-拼音映射
│   │
│   └── main.py              # 主程序（调度爬虫、处理、存储）
│
├── scripts/                 # 脚本目录
│   ├── run_history_crawl.py # 单独运行历史数据爬取
│   ├── run_realtime_crawl.py# 单独运行实时数据爬取
│   └── scheduled_crawl.py   # 定时采集脚本（实时数据每小时一次）
│
├── aqi_crawl.log            # aqi请求日志
├── aqi_realtime_crawl.log   # 实时爬取日志
├── history_crawl.log        # 历史爬取日志
├── requirements.txt         # 依赖包列表
├── chromedriver.exe         # 需要selenium代码运行时的本地Google驱动
├── README.md                # 项目说明文档
└── .gitignore               # Git忽略文件
```


## 三、核心配置文件
### 1. config/settings.py（全局配置）
```python
import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 数据存储路径
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
NEWRAW_DATA_DIR = os.path.join(BASE_DIR, "data", "Newraw")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
DATABASE_PATH = os.path.join(BASE_DIR, "data", "aqi_database.db")
# 是否将清洗/爬取的数据同时写入 SQLite（默认 False）
SAVE_TO_SQLITE = True


# 爬虫配置
REQUEST_INTERVAL = 2  # 请求间隔（秒），避免反爬
MAX_RETRY_TIMES = 3  # 请求失败重试次数
USER_AGENT_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36"
]

# 历史数据配置
START_YEAR = 2015  # 起始年份
END_YEAR = 2024    # 结束年份（可修改为当前年份）
HISTORY_CRAWL_BATCH_SIZE = 10  # 每次爬取10个城市后保存

# 实时数据配置
REALTIME_CRAWL_INTERVAL = 3600  # 实时数据采集间隔（秒）=1小时
REALTIME_CITIES = ["北京市", "上海市", "广州市", "深圳市", "天津市"]  # 优先爬取的重点城市

# 日志配置
LOG_LEVEL = "INFO"
LOG_FILE = os.path.join(BASE_DIR, "aqi_crawl.log")
# 专门用于数据库操作的日志（中文，位于仓库根）
DB_OP_LOG = os.path.join(BASE_DIR, "db_operations.log")

# 创建目录（若不存在）
for dir_path in [RAW_DATA_DIR, NEWRAW_DATA_DIR, PROCESSED_DATA_DIR]:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
```

### 2. config/cities.json（城市列表示例）
```json
{
  "直辖市": [
    {"name": "北京", "pinyin": "beijing"},
    {"name": "上海", "pinyin": "shanghai"},
    {"name": "天津", "pinyin": "tianjin"},
    {"name": "重庆", "pinyin": "chongqing"}
  ],
  "广东省": [
    {"name": "广州", "pinyin": "guangzhou"},
    {"name": "深圳", "pinyin": "shenzhen"},
    {"name": "东莞", "pinyin": "dongguan"}
  ],
  "江苏省": [
    {"name": "南京", "pinyin": "nanjing"},
    {"name": "苏州", "pinyin": "suzhou"}
  ]
  // 完整文件需包含全国所有地级市，可从网上下载城市列表后转换
}
```

## 四、核心代码实现
本节列举核心模块实现要点：

- `src/data_processing/storage.py`：现在支持 CSV 导出与 SQLite 写入（自动建表、类型推断、事务批量写入、查询接口）。数据库相关操作的日志会写入仓库根目录的 `db_operations.log`（中文）。
- `src/data_processing/cleaner.py`：提供 `clean_realtime(df)` 与 `clean_history(df)` 两个清洗函数，并支持通过 `src.main` 的 `clean_history` / `clean_realtime` / `clean` 命令对 `data/raw` 与 `data/Newraw` 目录批量清洗。
- `scripts/query_db.py`：交互式 REPL 与命令行模式查询工具，支持 `--list`、`--info`、`--sql`、`--export` 等，已本地化为中文提示，并将导出/错误写入 `db_operations.log`。
- `scripts/sync_csv_to_db.py`：把 `data/Newraw` 导入 `realtime_data` 表、`data/raw` 导入 `history_data` 表，支持 `--dry-run` 预览并生成导入统计，导入前建议先备份 `data/aqi_database.db`。
- `src/main.py`：增加了 `clean_history`、`clean_realtime` 与 `clean` 命令，并保留 `query`、`sync` 等命令的脚本转发实现。

示例模块与代码片段如下：
### 1. src/utils/request_utils.py（请求工具，抗反爬）
```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config.settings import MAX_RETRY_TIMES, USER_AGENT_POOL
import random
import time

def create_session():
    """创建支持重试和长连接的session"""
    session = requests.Session()
    retry_strategy = Retry(
        total=MAX_RETRY_TIMES,
        backoff_factor=1,  # 重试间隔：1s, 2s, 4s...
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=10, pool_maxsize=10)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def get_headers():
    """随机生成请求头"""
    return {
        "User-Agent": random.choice(USER_AGENT_POOL),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Referer": "https://www.aqistudy.cn/",
        "Connection": "keep-alive"
    }

def safe_get(session, url, params=None, timeout=15):
    """安全请求：自动重试、随机间隔、伪装头"""
    time.sleep(random.uniform(0.5, 1.5))  # 随机间隔，避免反爬
    try:
        response = session.get(
            url=url,
            params=params,
            headers=get_headers(),
            timeout=timeout,
            verify=False  # 忽略SSL验证（部分网站可能证书过期）
        )
        response.raise_for_status()  # 触发HTTP错误
        response.encoding = response.apparent_encoding or "utf-8"
        return response
    except Exception as e:
        print(f"请求失败：{url}，错误：{str(e)}")
        return None
```

### 2. src/crawlers/aqi_history.py（历史数据爬虫，aqistudy.cn）
```python
from src.utils.request_utils import create_session, safe_get
from config.settings import START_YEAR, END_YEAR, REQUEST_INTERVAL, RAW_DATA_DIR
from src.utils.city_mapper import get_all_cities
from src.data_processing.storage import save_raw_data
import pandas as pd
from bs4 import BeautifulSoup
import time

class AQIHistoryCrawler:
    def __init__(self):
        self.session = create_session()
        self.base_url = "https://www.aqistudy.cn/historydata/daydata.php"
        self.cities = get_all_cities()  # 获取所有城市（中文名+拼音）

    # （略）上文已说明 crawl_city_year_data 与 crawl_all 的实现，若需要完整代码请参考仓库中的 `src/crawlers/aqi_history.py`。

```

### 3. 补充：实时爬虫示例（完整）
下面给出 `src/crawlers/aqi_realtime.py` 的完整示例实现（含批量保存与可选 SQLite 写入）：

```python
from src.utils.request_utils import create_session, safe_get
from config.settings import REALTIME_CITIES, NEWRAW_DATA_DIR, SAVE_TO_SQLITE
from src.data_processing.storage import save_raw_data
import pandas as pd
from datetime import datetime
import time
import os
from src.utils.logger import setup_logger

logger = setup_logger("aqi_realtime")


class AQIRealtimeCrawler:
    def __init__(self):
        self.session = create_session()
        self.realtime_api = "http://www.cnemc.cn/sssj/ajax/airQualityHourData"

    def crawl_city_realtime(self, city_name):
        current_date = datetime.now().strftime("%Y-%m-%d")
        params = {"city": city_name, "date": current_date, "_": int(time.time() * 1000)}
        logger.info(f"请求实时接口：{city_name} {current_date}")
        resp = safe_get(self.session, self.realtime_api, params=params)
        if not resp:
            logger.warning(f"{city_name} 请求失败或无响应")
            return None
        try:
            data = resp.json()
        except Exception as e:
            logger.exception(f"解析 JSON 失败：{e}")
            return None

        records = []
        for hour_block in data.get("hourData", []):
            hour = hour_block.get("hour")
            for s in hour_block.get("stations", []):
                records.append({
                    "城市": city_name,
                    "日期": current_date,
                    "小时": hour,
                    "监测站点": s.get("stationName"),
                    "AQI": s.get("aqi"),
                    "PM2.5": s.get("pm25"),
                    "PM10": s.get("pm10"),
                    "SO₂": s.get("so2"),
                    "NO₂": s.get("no2"),
                    "CO": s.get("co"),
                    "O₃": s.get("o3"),
                    "首要污染物": s.get("primaryPollutant"),
                    "采集时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

        if not records:
            logger.info(f"{city_name} 无实时数据")
            return None
        return pd.DataFrame(records)

    def crawl_realtime_batch(self, cities=None, save_dir=None):
        cities = cities or REALTIME_CITIES
        save_dir = save_dir or NEWRAW_DATA_DIR
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        all_dfs = []
        for city in cities:
            df = self.crawl_city_realtime(city)
            if df is None:
                continue
            all_dfs.append(df)
            fname = f"realtime_{city}_{ts}.csv"
            fpath = os.path.join(save_dir, fname)
            os.makedirs(os.path.dirname(fpath), exist_ok=True)
            df.to_csv(fpath, index=False, encoding='utf-8-sig')
            logger.info(f"已保存：{fpath}")
            if SAVE_TO_SQLITE:
                try:
                    save_raw_data(df, filename=fname, table_name='realtime_data')
                except Exception:
                    logger.exception("写入 SQLite 失败")
            time.sleep(1 + (0.5 * (os.getpid() % 3)))  # 简单抖动

        if all_dfs:
            combined = pd.concat(all_dfs, ignore_index=True)
            logger.info(f"批量爬取完成，共 {len(combined)} 条记录")
            return combined
        logger.info("未获取到任何实时数据")
        return None


if __name__ == '__main__':
    c = AQIRealtimeCrawler()
    c.crawl_realtime_batch()

```

### 使用示例（快速）

- 运行实时爬取（模块方式，推荐）：

```powershell
python -m src.main realtime
```

- 运行历史爬取（全部城市，可能较慢）：

```powershell
python -m src.main history
```

### 常见排查要点

- 日志重复或双写：确认是否有模块在导入时设置了 root handler（`logging.basicConfig`），可将模块日志 `propagate=False` 或移除根级 basicConfig。
- 403 / 反爬：先减缓请求速率，临时移除或更换代理，必要时用 Selenium 渲染页面。
- 写入 SQLite 报错：先导出 CSV 检查列名，再用 `src.data_processing.cleaner` 规范列名后导入。

---

若你希望，我可以继续：
- 把 `src/main.py` 的 `realtime` / `history` 命令示例补成可运行的 CLI；
- 或在你的环境跑一次 `python -m src.main realtime` 并把终端日志摘录回来便于进一步定位问题（例如仍然出现重复日志或 403/超时）。


    def crawl_city_year_data(self, city_pinyin, city_name, year):
        """爬取单个城市单个年份的每日AQI数据"""
        all_daily_data = []
        # 构造URL：https://www.aqistudy.cn/historydata/daydata.php?city=beijing&year=2023
        params = {"city": city_pinyin, "year": year}
        response = safe_get(self.session, self.base_url, params=params)
        
        if not response:
            return None
        
        soup = BeautifulSoup(response.text, "lxml")
        table = soup.find("table", class_="table table-condensed table-bordered table-striped table-hover")
        
        if not table:
            print(f"未找到{city_name}{year}年数据")
            return None
        
        # 解析表头
        headers = [th.text.strip() for th in table.find_all("th")]
        # 解析表体数据
        rows = table.find_all("tr")[1:]  # 跳过表头行
        for row in rows:
            cols = [td.text.strip() for td in row.find_all("td")]
            if len(cols) == len(headers):
                daily_data = dict(zip(headers, cols))
                daily_data["城市"] = city_name
                daily_data["年份"] = year
                all_daily_data.append(daily_data)
        
        # 转换为DataFrame并处理数据类型
        df = pd.DataFrame(all_daily_data)
        if not df.empty:
            # 转换数值列（处理"-"为NaN）
            numeric_cols = ["AQI", "PM2.5", "PM10", "SO₂", "NO₂", "CO", "O₃", "排名"]
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col].replace("-", None), errors="coerce")
            return df
        return None

    def crawl_all(self, batch_size=None):
        """爬取所有城市所有年份数据（支持批量保存）"""
        batch_count = 0
        batch_data = []
        batch_size = batch_size or 10  # 默认每10个城市保存一次
        
        for province, city_list in self.cities.items():
            print(f"\n开始爬取{province}数据...")
            for city in city_list:
                city_name = city["name"]
                city_pinyin = city["pinyin"]
                print(f"正在爬取 {city_name}（{city_pinyin}）...")

---

## 结语

本文档为项目设计与实现说明，旨在帮助开发者快速理解项目架构、配置要点与使用方式。若你打算在生产环境长期运行该项目，建议：

- 为爬虫添加更完善的异常恢复与监控（告警、重试策略、速率限制）。
- 审核目标网站的使用条款与 robots.txt，遵守法律与道德规范。
- 将敏感或大规模数据持久化到更可靠的存储（如托管数据库），并做好备份策略。
- 添加 CI / 单元测试覆盖关键数据处理逻辑，确保清洗规则稳定。

如需我将 `src/main.py` 补成更完整的 CLI、或为 `scripts/` 添加演示命令和测试用例，我可以继续实现并运行本地验证。 
                
                for year in range(START_YEAR, END_YEAR + 1):
                    df = self.crawl_city_year_data(city_pinyin, city_name, year)
                    if df is not None and not df.empty:
                        batch_data.append(df)
                        print(f"成功爬取{city_name}{year}年数据，共{len(df)}条")
                
                time.sleep(REQUEST_INTERVAL)  # 城市间间隔
                batch_count += 1
                
                # 批量保存
                if batch_count >= batch_size:
                    self._save_batch(batch_data)
                    batch_data = []
                    batch_count = 0
        
        # 保存剩余数据
        if batch_data:
            self._save_batch(batch_data)

    def _save_batch(self, batch_data):
        """批量保存数据到CSV"""
        if not batch_data:
            return
        combined_df = pd.concat(batch_data, ignore_index=True)
        # 按年份+城市分组保存
        for (year, city), df in combined_df.groupby(["年份", "城市"]):
            filename = f"{year}_{city}_aqi_history.csv"
            file_path = os.path.join(RAW_DATA_DIR, filename)
            df.to_csv(file_path, index=False, encoding="utf-8-sig")
        print(f"批量保存完成，共{len(combined_df)}条数据")

if __name__ == "__main__":
    crawler = AQIHistoryCrawler()
    crawler.crawl_all(batch_size=HISTORY_CRAWL_BATCH_SIZE)
```

### 3. src/crawlers/aqi_realtime.py（实时数据爬虫，cnemc.cn）
```python
from src.utils.request_utils import create_session, safe_get
from config.settings import REALTIME_CITIES, RAW_DATA_DIR
from src.data_processing.storage import save_raw_data
import pandas as pd
from bs4 import BeautifulSoup
import time
from datetime import datetime

class AQIRealtimeCrawler:
    def __init__(self):
        self.session = create_session()
        self.base_url = "http://www.cnemc.cn/sssj/"
        self.realtime_api = "http://www.cnemc.cn/sssj/ajax/airQualityHourData"  # 实时数据接口

    def crawl_city_realtime(self, city_name):
        """爬取单个城市的实时AQI数据（逐小时）"""
        current_date = datetime.now().strftime("%Y-%m-%d")
        params = {
            "city": city_name,
            "date": current_date,
            "_": int(time.time() * 1000)  # 时间戳防缓存
        }
        
        response = safe_get(self.session, self.realtime_api, params=params)
        if not response:
            return None
        
        try:
            data = response.json()
        except Exception as e:
            print(f"解析{city_name}实时数据失败：{str(e)}")
            return None
        
        # 解析数据
        all_station_data = []
        for hour_data in data.get("hourData", []):
            hour = hour_data.get("hour", "")
            for station in hour_data.get("stations", []):
                station_data = {
                    "城市": city_name,
                    "日期": current_date,
                    "小时": hour,
                    "监测站点": station.get("stationName", ""),
                    "AQI": pd.to_numeric(station.get("aqi", None), errors="coerce") if station.get("aqi") != "-" else None,
                    "空气质量等级": station.get("quality", ""),
                    "PM2.5": pd.to_numeric(station.get("pm25", None), errors="coerce") if station.get("pm25") != "-" else None,
                    "PM10": pd.to_numeric(station.get("pm10", None), errors="coerce") if station.get("pm10") != "-" else None,
                    "SO₂": pd.to_numeric(station.get("so2", None), errors="coerce") if station.get("so2") != "-" else None,
                    "NO₂": pd.to_numeric(station.get("no2", None), errors="coerce") if station.get("no2") != "-" else None,
                    "CO": pd.to_numeric(station.get("co", None), errors="coerce") if station.get("co") != "-" else None,
                    "O₃": pd.to_numeric(station.get("o3", None), errors="coerce") if station.get("o3") != "-" else None,
                    "首要污染物": station.get("primaryPollutant", ""),
                    "采集时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                all_station_data.append(station_data)
        
        return pd.DataFrame(all_station_data)

    def crawl_realtime_batch(self, cities=None):
        """批量爬取多个城市的实时数据"""
        cities = cities or REALTIME_CITIES
        all_realtime_data = []
        
        print(f"开始爬取实时AQI数据（{datetime.now().strftime('%Y-%m-%d %H:%M')}）")
        for city in cities:
            df = self.crawl_city_realtime(city)