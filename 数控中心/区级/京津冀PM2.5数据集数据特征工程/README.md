# 全国 AQI 数据采集系统

本仓库为一个示例性项目，用于采集中国城市的 AQI（空气质量）历史与实时数据，包含：爬虫、数据清洗、合并、CSV/SQLite 存储与交互查询工具。

主要特性
- 历史数据爬取：按年份和城市抓取并保存为 CSV。
- 实时数据爬取：逐小时抓取站点级实时数据。
- 数据清洗：统一列名、去重、缺失值填充（`src/data_processing/cleaner.py`）。
- 存储：CSV 为主；支持将数据写入本地 SQLite 数据库（`src/data_processing/storage.py`）。
- 交互查询：`scripts/query_db.py` 提供 REPL 与导出功能。
- 同步工具：`scripts/sync_csv_to_db.py` 支持把 `data/` 下的 CSV 同步导入数据库（支持 `--dry-run`）。

快速开始（Windows / PowerShell）
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

运行示例
```powershell
# 查看 CLI 用法
python -m src.main

# 历史爬取
python -m src.main history

# 单次实时爬取
python -m src.main realtime

# 定时实时爬取（按配置间隔，按 Ctrl+C 停止）
python -m src.main scheduled

# 交互式数据库查询
python -m src.main query

# 同步 data 下 CSV 到 SQLite（dry-run 预览）
python -m src.main sync --target both --dry-run

# 清洗：历史/实时/同时
python -m src.main clean_history
python -m src.main clean_realtime
python -m src.main clean
```

配置与日志（概览）
- 配置文件位于 `config/settings.py`，其中定义了 `RAW_DATA_DIR`、`NEWRAW_DATA_DIR`、`PROCESSED_DATA_DIR`、`DATABASE_PATH`、`SAVE_TO_SQLITE` 等。
- 数据库写入由 `src/data_processing/storage.py` 的 `save_to_sqlite` 控制，是否启用可通过 `config/settings.py` 中 `SAVE_TO_SQLITE` 打开/关闭。
- 所有数据库相关的操作（插入、查询、导出、错误）会记录到仓库根目录的 `db_operations.log`（中文日志），便于审计与排查。

# 全国 AQI 数据采集系统

一个用于采集中国城市 AQI（空气质量）历史与实时数据的示例性 Python 项目。包含爬虫、数据清洗、合并、CSV 与 SQLite 存储，以及交互式查询与同步脚本，便于用于学习、研究或作为工程骨架二次开发。

主要功能
- 历史数据爬取：按城市与年份抓取并保存为 CSV。
- 实时数据爬取：逐小时抓取站点级实时数据并保存备份。
- 数据清洗：统一列名、去重、缺失值处理（见 `src/data_processing/cleaner.py`）。
- 存储与同步：CSV 为主，同时支持将数据写入 SQLite（见 `src/data_processing/storage.py` 与 `scripts/sync_csv_to_db.py`）。
- 交互查询：`scripts/query_db.py` 提供 REPL 与导出功能。

快速开始（Windows / PowerShell）
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

跨平台（Linux / macOS）
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

常用运行示例
```powershell
# 查看模块化 CLI 帮助
python -m src.main

# 运行历史数据爬取
python -m src.main history

# 运行单次实时爬取
python -m src.main realtime

# 启动定时实时爬取（按 Ctrl+C 停止）
python -m src.main scheduled

# 交互式数据库查询
python -m src.main query

# 同步 data 下 CSV 到 SQLite（dry-run 预览）
python -m src.main sync --target both --dry-run

# 清洗：历史/实时/同时
python -m src.main clean_history
python -m src.main clean_realtime
python -m src.main clean
```

项目结构（概览）
- `config/`：配置（`settings.py`、城市列表等）
- `data/`：数据目录（`raw/`、`Newraw/`、`processed/`、数据库备份）
- `src/`：代码主目录（`crawlers/`、`data_processing/`、`utils/`、`main.py`）
- `scripts/`：辅助脚本（爬取、同步、查询等）

配置与日志
- 全局配置在 `config/settings.py`，包含数据路径、爬取间隔、是否写入 SQLite 等。
- 数据库写入由 `src/data_processing/storage.py` 控制；操作日志集中记录到仓库根目录的 `db_operations.log`，便于审计与排查。

更多细节
- 更完整的实现说明、配置示例与模块细节请参见 `readme02.md`。

贡献与许可
- 本仓库为示例项目，欢迎提交 issue 或 PR 改进爬取稳定性、错误处理与文档。
- 若需用于生产或公开发布，请先添加或确认 LICENSE 文件并根据目标网站的 robots 与使用条款调整爬取策略。

---

示例项目 — 仅供学习与参考。
```



**目录说明**
