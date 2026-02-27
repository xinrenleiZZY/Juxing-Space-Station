import os
import time
from typing import Optional

import pandas as pd
import logging

from config.settings import PROCESSED_DATA_DIR, DATABASE_PATH, SAVE_TO_SQLITE, RAW_DATA_DIR, NEWRAW_DATA_DIR
from src.data_processing.storage import save_to_sqlite

# 使用与 storage 相同的日志记录器，写入仓库根目录的 db_operations.log
logger = logging.getLogger("db_operations")


def _ensure_processed_dir():
    if not os.path.exists(PROCESSED_DATA_DIR):
        os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)


def _select_first(df: pd.DataFrame, candidates: list) -> Optional[str]:
    """从候选列名中选第一个存在于 df.columns 的列名，找不到返回 None。"""
    for c in candidates:
        if c in df.columns:
            return c
    return None


def _save_processed(df: pd.DataFrame, basename: str, table_name: str) -> None:
    """保存清洗后的数据到 `processed/` 目录和 SQLite 表。

    - `basename` 不应包含目录（只文件名），脚本会在前面加时间戳。
    - `table_name` 是写入数据库的表名。
    """
    if df is None or df.empty:
        return
    _ensure_processed_dir()
    ts = time.strftime("%Y%m%d_%H%M%S")
    fname = f"{ts}_{basename}"
    csv_path = os.path.join(PROCESSED_DATA_DIR, fname)
    try:
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        logger.info(f"已保存清洗后的 CSV：{csv_path}")
        print(f"已保存清洗后的 CSV：{csv_path}")
    except Exception as e:
        logger.exception(f"写入清洗后 CSV 失败：{csv_path} -> {e}")
        print(f"写入清洗后 CSV 失败：{csv_path}：{e}")

    try:
        n = save_to_sqlite(df, table_name=table_name)
        if n is not None:
            logger.info(f"已保存 {n} 行到数据库表 '{table_name}'")
            print(f"已保存 {n} 行到数据库表 '{table_name}'")
    except Exception as e:
        logger.exception(f"写入数据库表 '{table_name}' 失败：{e}")
        print(f"写入数据库表 '{table_name}' 失败：{e}")


def clean_realtime(df: pd.DataFrame, save_individual: bool = False) -> pd.DataFrame:
    """清洗实时数据，保留并规范化列：
    城市、日期、小时、AQI、空气质量等级、PM2.5
    返回清洗后的 DataFrame（列顺序固定）。
    
    Args:
        df: 待清洗的 DataFrame
        save_individual: 是否保存单个文件（默认不保存）
    """
    if df is None or df.empty:
        return df

    df = df.copy()
    # 常见列名候选
    col_city = _select_first(df, ["城市", "city", "city_name"])
    col_date = _select_first(df, ["日期", "date"])
    col_hour = _select_first(df, ["小时", "hour"])
    col_aqi = _select_first(df, ["AQI", "aqi", "指数"])
    col_level = _select_first(df, ["空气质量等级", "质量等级", "等级", "quality"])
    col_pm25 = _select_first(df, ["PM2.5", "PM2_5", "pm25"])

    # 构建输出 df
    out = pd.DataFrame()
    out["城市"] = df[col_city] if col_city else None
    out["日期"] = df[col_date] if col_date else None
    out["小时"] = df[col_hour] if col_hour else None
    out["AQI"] = pd.to_numeric(df[col_aqi], errors="coerce") if col_aqi else None
    out["空气质量等级"] = df[col_level] if col_level else None
    out["PM2.5"] = pd.to_numeric(df[col_pm25], errors="coerce") if col_pm25 else None

    # 去重（按城市+日期+小时+监测站点/若无则按城市+日期+小时）
    if "监测站点" in df.columns:
        out["监测站点"] = df["监测站点"]
        out = out.drop_duplicates(subset=[c for c in ["城市", "日期", "小时", "监测站点"] if c in out.columns])
    else:
        out = out.drop_duplicates(subset=[c for c in ["城市", "日期", "小时"] if c in out.columns])

    # 填充数值列中位数（可选）
    for col in ["AQI", "PM2.5"]:
        if col in out.columns:
            median = pd.to_numeric(out[col], errors="coerce").median()
            out[col] = pd.to_numeric(out[col], errors="coerce").fillna(median)

    # 保存单个文件（可选）
    if save_individual:
        _save_processed(out, "realtime_processed.csv", "realtime_processed")
    return out


def clean_history(df: pd.DataFrame, save_individual: bool = False) -> pd.DataFrame:
    """清洗历史数据，保留并规范化列：城市、日期、小时、AQI、空气质量等级、PM2.5
    返回清洗后的 DataFrame（列顺序固定）。
    
    Args:
        df: 待清洗的 DataFrame
        save_individual: 是否保存单个文件（默认不保存）
    """
    if df is None or df.empty:
        return df

    df = df.copy()
    col_city = _select_first(df, ["城市", "city", "city_name"])
    col_date = _select_first(df, ["日期", "date", "day", "时间"])  # 历史可能是具体日期
    col_aqi = _select_first(df, ["AQI指数", "AQI", "aqi", "指数"])  # 优先使用AQI指数
    col_level = _select_first(df, ["质量等级", "空气质量等级", "等级", "quality"])  # 优先使用质量等级
    col_pm25 = _select_first(df, ["PM2.5", "PM2_5", "pm25"])

    out = pd.DataFrame()
    out["城市"] = df[col_city] if col_city else None
    out["日期"] = df[col_date] if col_date else None
    out["小时"] = None  # 历史数据没有小时，留空
    out["AQI"] = pd.to_numeric(df[col_aqi], errors="coerce") if col_aqi else None
    out["空气质量等级"] = df[col_level] if col_level else None  # 重命名为空气质量等级
    out["PM2.5"] = pd.to_numeric(df[col_pm25], errors="coerce") if col_pm25 else None

    # 去重（按城市+日期）
    out = out.drop_duplicates(subset=[c for c in ["城市", "日期"] if c in out.columns])

    # 填充数值列中位数
    for col in ["AQI", "PM2.5"]:
        if col in out.columns:
            median = pd.to_numeric(out[col], errors="coerce").median()
            out[col] = pd.to_numeric(out[col], errors="coerce").fillna(median)

    # 保存单个文件（可选）
    if save_individual:
        _save_processed(out, "history_processed.csv", "history_processed")
    return out


__all__ = ["clean_realtime", "clean_history"]
