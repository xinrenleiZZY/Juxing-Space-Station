#!/usr/bin/env python
"""将 data 下的 CSV 文件同步到 SQLite 数据库的脚本

功能说明：
- 把 `data/Newraw/` 目录下的实时数据 CSV 同步到 `realtime_data` 表
- 把 `data/Hisraw/` 目录下的历史数据 CSV 同步到 `history_data` 表
- 支持去重操作，避免重复数据插入
- 提供 dry-run 模式，用于预览同步效果

用法示例：
    python scripts/sync_csv_to_db.py --target both
    python scripts/sync_csv_to_db.py --target realtime --dry-run
    python scripts/sync_csv_to_db.py --target history
"""
import sys
import os
import argparse
from glob import glob

# 确保项目根目录在 Python 路径中，以便正确导入模块
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import pandas as pd
from config.settings import RAW_DATA_DIR, NEWRAW_DATA_DIR
from src.data_processing.storage import save_to_sqlite, query_sqlite, save_raw_data
import logging

# 使用 storage 模块已配置的日志文件，确保日志记录一致
logger = logging.getLogger("db_operations")



def _read_csv(path):
    """读取 CSV 文件，自动处理编码问题
    
    参数:
        path: CSV 文件路径
    
    返回:
        pandas.DataFrame: 读取的数据框
    """
    try:
        # 优先使用 UTF-8 with BOM 编码
        return pd.read_csv(path, encoding='utf-8-sig')
    except Exception:
        # 失败时尝试普通 UTF-8 编码，忽略错误
        return pd.read_csv(path, encoding='utf-8', errors='ignore')



def _build_key(df, cols):
    """构建用于去重的键值
    
    参数:
        df: pandas.DataFrame，包含数据的 DataFrame
        cols: list，用于构建键的列名列表
    
    返回:
        pandas.Series: 包含键值的 Series
    """
    # 将指定列的值用 | 连接，生成唯一键字符串
    return df[cols].fillna('').astype(str).agg('|'.join, axis=1)



def sync_folder_to_table(folder, table_name, prefer_keys=None, dry_run=False):
    """将指定目录下的所有 CSV 文件同步到数据库表
    
    参数:
        folder: str，包含 CSV 文件的目录路径
        table_name: str，目标数据库表名
        prefer_keys: list, optional，用于去重的首选列名列表
        dry_run: bool, optional，是否启用 dry-run 模式（仅预览不实际插入）
    """
    # 获取目录下所有 CSV 文件
    files = glob(os.path.join(folder, '*.csv'))
    if not files:
        logger.info(f'目录没有 CSV 文件：{folder}')
        return

    logger.info(f'发现 {len(files)} 个 CSV 文件在 {folder} -> 目标表: {table_name}')

    # 尝试加载数据库中已存在的键值（用于去重）
    existing_keys = set()
    if prefer_keys:
        # 构建 SQL 查询语句，获取去重所需的列
        cols_sql = ','.join([f'"{c}"' for c in prefer_keys])
        try:
            # 查询数据库中已存在的数据
            df_exist = query_sqlite(f'SELECT {cols_sql} FROM {table_name}')
            if df_exist is not None and not df_exist.empty:
                # 生成现有数据的键值集合
                existing_keys = set(df_exist.fillna('').astype(str).agg('|'.join, axis=1).tolist())
        except Exception:
            # 如果查询失败，使用空集合（不进行去重）
            existing_keys = set()

    total_inserted = 0
    # 遍历处理每个 CSV 文件
    for p in files:
        logger.info(f'开始处理：{p}')
        df = _read_csv(p)
        if df is None or df.empty:
            logger.info('  文件为空，跳过')
            continue

        # 选择用于去重的键列
        if prefer_keys:
            # 只使用文件中存在的首选键列
            keys = [c for c in prefer_keys if c in df.columns]
        else:
            # 如果没有指定首选键列，使用所有列
            keys = list(df.columns)

        if not keys:
            # 如果没有可用列，使用整行数据作为键
            df['_sync_key'] = df.astype(str).agg('|'.join, axis=1)
            keys = ['_sync_key']
        else:
            # 使用指定的键列生成键值
            df['_sync_key'] = _build_key(df, keys)

        # 筛选出数据库中不存在的新行
        if existing_keys:
            mask_new = ~df['_sync_key'].isin(existing_keys)
        else:
            # 如果没有现有键，所有行都是新行
            mask_new = [True] * len(df)

        new_rows = df[mask_new].drop(columns=['_sync_key'])
        logger.info(f'  总行数: {len(df)}, 新行数: {len(new_rows)}')

        if len(new_rows) == 0:
            # 没有新数据，跳过
            continue

        if dry_run:
            # dry-run 模式，仅预览插入效果
            logger.info('  dry-run 模式，未执行写入')
            total_inserted += len(new_rows)
            # 更新模拟的现有键集合
            existing_keys.update(df.loc[mask_new, '_sync_key'].tolist())
            continue

        # 将新数据插入数据库
        try:
            n = save_to_sqlite(new_rows, table_name=table_name)
            logger.info(f'  已插入 {n} 行到 {table_name}')
            total_inserted += n
            # 更新现有键集合，避免后续文件重复插入
            existing_keys.update(df.loc[mask_new, '_sync_key'].tolist())
        except Exception as e:
            # 记录插入失败的异常信息
            logger.exception(f'  插入失败：{e}')

    logger.info(f'\n完成同步 {folder} -> {table_name}, total_inserted={total_inserted}')



def main():
    """主函数，解析命令行参数并执行同步操作
    """
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='Sync CSV files to SQLite tables')
    parser.add_argument('--target', choices=['realtime', 'history', 'both'], 
                        default='both', help='指定要同步的数据类型')
    parser.add_argument('--dry-run', action='store_true', 
                        help='启用 dry-run 模式，仅预览同步效果不实际插入')
    args = parser.parse_args()

    # 根据参数选择同步实时数据
    if args.target in ('realtime', 'both'):
        # 实时数据的去重键：城市、日期、小时、监测站点
        prefer_keys_rt = ['城市', '日期', '小时', '监测站点']
        sync_folder_to_table(NEWRAW_DATA_DIR, 'realtime_data', 
                           prefer_keys=prefer_keys_rt, dry_run=args.dry_run)

    # 根据参数选择同步历史数据
    if args.target in ('history', 'both'):
        # 历史数据的去重键：城市、年份、月份
        prefer_keys_hist = ['城市', '年份', '月份']
        sync_folder_to_table(RAW_DATA_DIR, 'history_data', 
                           prefer_keys=prefer_keys_hist, dry_run=args.dry_run)


if __name__ == '__main__':
    # 脚本入口点
    main()
