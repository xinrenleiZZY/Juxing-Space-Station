import os
import sqlite3
from typing import Optional, Any

import logging
import pandas as pd

from config.settings import DATABASE_PATH, RAW_DATA_DIR

# 配置数据库操作专用 logger，避免在模块导入时修改根 logger 的 handlers
# 这样可以防止其他模块（例如爬虫模块）配置的 console 日志被覆盖或失效。
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_LOG_PATH = os.path.join(PROJECT_ROOT, "db_operations.log")



def _ensure_dir(path: str):
    """确保给定路径的目录存在。

    如果提供的是文件路径（例如包含扩展名或有父目录），则创建父目录；
    如果提供的是目录路径，则直接创建该目录。
    """
    if not path:
        return
    # 如果 path 看起来像目录（以分隔符结尾）则直接使用，否则取父目录
    if path.endswith(os.sep) or path.endswith('/'):
        dirpath = path
    else:
        dirpath = os.path.dirname(path) or path

    if not dirpath:
        return
    if not os.path.exists(dirpath):
        os.makedirs(dirpath, exist_ok=True)

logger = logging.getLogger("db_operations")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    _fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh = logging.FileHandler(DB_LOG_PATH, encoding='utf-8')
    fh.setFormatter(_fmt)
    sh = logging.StreamHandler()
    sh.setFormatter(_fmt)
    logger.addHandler(fh)
    logger.addHandler(sh)
    # 防止日志消息向上传播到 root logger（避免重复输出）
    logger.propagate = False

def _get_conn(db_path: str = DATABASE_PATH) -> sqlite3.Connection:
    _ensure_dir(db_path)
    conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    # 性能/并发优化
    try:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
    except Exception:
        pass
    return conn


def init_db(db_path: str = DATABASE_PATH):
    """初始化数据库（创建目录并设置基本PRAGMA）。"""
    conn = _get_conn(db_path)
    conn.close()
    logger.info(f"🌐 已初始化数据库（路径：{db_path}）")


def _infer_sqlite_type(series: pd.Series) -> str:
    if pd.api.types.is_integer_dtype(series):
        return "INTEGER"
    if pd.api.types.is_float_dtype(series):
        return "REAL"
    if pd.api.types.is_bool_dtype(series):
        return "INTEGER"
    # datetime -> TEXT (ISO格式)
    if pd.api.types.is_datetime64_any_dtype(series):
        return "TEXT"
    return "TEXT"


def _create_table_if_not_exists(conn: sqlite3.Connection, table_name: str, df: pd.DataFrame):
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    if cur.fetchone():
        return

    cols = []
    for col in df.columns:
        col_type = _infer_sqlite_type(df[col])
        safe_col = str(col).replace('"', '""')
        cols.append(f'"{safe_col}" {col_type}')

    cols_def = ", ".join(cols)
    sql = f'CREATE TABLE IF NOT EXISTS "{table_name}" (id INTEGER PRIMARY KEY AUTOINCREMENT, {cols_def})'
    cur.execute(sql)
    conn.commit()


def save_to_sqlite(df: pd.DataFrame, table_name: str, db_path: str = DATABASE_PATH, if_exists: str = "append", chunksize: int = 500):
    """将 DataFrame 保存到 SQLite。自动建表（首次写入），并使用事务批量插入。

    注意：列名会按 DataFrame 的列顺序写入，空值转换为 NULL。
    """
    if df is None or df.empty:
        return 0

    # 保持列名为字符串
    df = df.copy()
    df.columns = [str(c) for c in df.columns]

    conn = _get_conn(db_path)
    try:
        _create_table_if_not_exists(conn, table_name, df)

        cols = [f'"{c.replace('"', '""')}"' for c in df.columns]
        placeholders = ",".join(["?" for _ in df.columns])
        insert_sql = f'INSERT INTO "{table_name}" ({",".join(cols)}) VALUES ({placeholders})'

        total = 0
        with conn:
            for start in range(0, len(df), chunksize):
                chunk = df.iloc[start:start + chunksize]
                values = [tuple(None if pd.isna(x) else x for x in row) for row in chunk.values.tolist()]
                conn.executemany(insert_sql, values)
                total += len(values)
        logger.info(f"📌 已将 {total} 条记录写入表 '{table_name}'（数据库：{db_path}）")
        return total
    except Exception as e:
        logger.exception(f"❌ 写入表 '{table_name}' 失败：{e}")
        raise
    finally:
        conn.close()


def save_raw_data(df: pd.DataFrame, filename: Optional[str] = None, table_name: str = "raw_data") -> Optional[str]:
    """保存原始 DataFrame 到 CSV（保留现有行为）并将数据写入 SQLite（可选表名）。

    返回 CSV 文件路径（或 None）。
    """
    if df is None or df.empty:
        return None

    # 支持传入绝对路径作为 filename；否则将文件写入 RAW_DATA_DIR
    if filename is None:
        filename = f"raw_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
    if os.path.isabs(filename):
        csv_path = filename
    else:
        csv_path = os.path.join(RAW_DATA_DIR, filename)
    logger.info("=" * 60)  # 分隔线
    logger.info(f"✅ 爬取数据完成！")
    logger.info(f"🔄 数据将同步执行：")
    logger.info(f"     ├─ 📌录入增量数据库")
    logger.info(f"     └─ 💾保存为CSV")
    # 确保父目录存在
    _ensure_dir(os.path.dirname(csv_path))
    try:
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        logger.info(f"💾 CSV 已保存：{csv_path}")
    except Exception as e:
        logger.exception(f"📍 写入 CSV 失败：{e}")

    try:
        saved = save_to_sqlite(df, table_name=table_name, db_path=DATABASE_PATH)
        if saved and saved > 0:
            logger.info(f"✅ 已写入 SQLite 表 '{table_name}'，记录数：{saved}")
    except Exception as e:
        logger.exception(f"⚠️ 写入 SQLite 失败：{e}")

    return csv_path


def query_sqlite(query: str, params: Optional[Any] = None, db_path: str = DATABASE_PATH) -> pd.DataFrame:
    """执行查询并返回 pandas.DataFrame。"""
    conn = _get_conn(db_path)
    try:
        df = pd.read_sql_query(query, conn, params=params)
        logger.info(f"🎯 已执行查询：{query}")
        return df
    except Exception as e:
        logger.exception(f"⚠️ 查询失败：{e}，SQL: {query}")
        raise
    finally:
        conn.close()


def list_tables(db_path: str = DATABASE_PATH) -> list:
    """列出数据库中的表名。"""
    conn = _get_conn(db_path)
    try:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [row[0] for row in cur.fetchall()]
        logger.info(f"数据库表列表：{tables}")
        return tables
    finally:
        conn.close()


def table_info(table_name: str, db_path: str = DATABASE_PATH) -> pd.DataFrame:
    """返回表的列信息（PRAGMA table_info）。"""
    conn = _get_conn(db_path)
    try:
        df = pd.read_sql_query(f"PRAGMA table_info('{table_name}')", conn)
        logger.info(f"表 {table_name} 的列信息已读取（{len(df)} 列）")
        return df
    finally:
        conn.close()

def view_db_table(table_name: str, limit: int = 100):
    """查询并打印数据库表内容"""
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        # 读取表数据
        df = pd.read_sql(f"SELECT * FROM {table_name} LIMIT {limit}", conn)
        logger.info(f"表 {table_name} 的前 {limit} 行数据已读取（共 {len(df)} 行）")
        return df
    except Exception as e:
        logger.exception(f"查询失败：{e}")
        return None
    finally:
        conn.close()


if __name__ == "__main__":
    # 提示用户不要直接运行此模块（会导致包导入失败），并给出正确的运行方式
    print("请不要直接运行此文件。建议在项目根目录以模块方式运行：")
    print("  python -m src.main")
    print("或运行交互查询工具：")
    print("  python -m src.data_processing.storage  # 作为模块运行（需在项目根目录执行）")
    print("如果你只是想在交互环境中导入该模块，请确保项目根目录在 PYTHONPATH 或 sys.path 中。")
    import sys
    sys.exit(1)