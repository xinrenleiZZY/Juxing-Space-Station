import os
import pandas as pd
from typing import Optional
from config.settings import RAW_DATA_DIR, NEWRAW_DATA_DIR, BASE_DIR
from src.data_processing.cleaner import clean_history as _clean_history, clean_realtime as _clean_realtime, _save_processed
from src.utils.logger import setup_logger


def run_clean_history(dir_path: str = None, merge_all: bool = True, log_file: str = None):
    """清洗历史数据：扫描 `data/Hisraw`（或指定目录）中的 CSV，逐文件调用 `clean_history` 并保存结果。
    
    Args:
        dir_path: 原始数据目录路径
        merge_all: 是否合并所有文件的清洗结果为一个文件
        log_file: 日志文件路径（可选）
    """
    try:
        from src.utils.logger import setup_logger
    except Exception as e:
        print(f"❌ 无法导入清洗模块：{e}")
        return
    
    # 设置日志
    logger = setup_logger("clean_history", log_file=log_file)
    logger.info("开始历史数据清洗操作")
    
    if dir_path is None:
        dir_path = RAW_DATA_DIR
    print(f"🚀 开始清洗历史数据，目录：{dir_path}")
    logger.info(f"清洗历史数据，目录：{dir_path}")
    
    count = 0
    success_count = 0
    all_cleaned_data = None
    
    for fname in os.listdir(dir_path):
        logger.info(f"发现文件：{fname}")
        print(f"🔍 发现文件：{fname}")
        if not fname.lower().endswith('.csv'):
            logger.debug(f"跳过非CSV文件：{fname}")
            continue
        
        fpath = os.path.join(dir_path, fname)
        try:
            df = pd.read_csv(fpath, encoding='utf-8-sig')
            logger.info(f"读取文件成功：{fpath}，共 {len(df)} 行数据")
            
            cleaned_df = _clean_history(df)
            count += 1
            success_count += 1
            logger.info(f"清洗文件成功：{fpath}")
            
            # 收集所有清洗后的数据
            if merge_all and cleaned_df is not None and not cleaned_df.empty:
                if all_cleaned_data is None:
                    all_cleaned_data = cleaned_df.copy()
                    logger.info(f"初始化合并数据集，当前数据量：{len(all_cleaned_data)} 行")
                else:
                    prev_count = len(all_cleaned_data)
                    all_cleaned_data = pd.concat([all_cleaned_data, cleaned_df], ignore_index=True)
                    # 去重
                    all_cleaned_data = all_cleaned_data.drop_duplicates(subset=[c for c in ["城市", "日期"] if c in all_cleaned_data.columns])
                    logger.info(f"合并数据：新增 {len(cleaned_df)} 行，合并后共 {len(all_cleaned_data)} 行，去重减少 {prev_count + len(cleaned_df) - len(all_cleaned_data)} 行")
                    
        except Exception as e:
            logger.error(f"清洗文件失败：{fpath} -> {e}")
            print(f"❌ 清洗文件失败：{fpath} -> {e}")
    
    # 保存合并后的结果
    if merge_all and all_cleaned_data is not None and not all_cleaned_data.empty:
        logger.info(f"开始合并 {success_count} 个文件的清洗结果，合并后共 {len(all_cleaned_data)} 行数据")
        print(f"📊 正在合并 {success_count} 个文件的清洗结果...")
        
        try:
            _save_processed(all_cleaned_data, "history_merged.csv", "history_merged")
            logger.info(f"合并后的历史数据已保存，共 {len(all_cleaned_data)} 行")
            print(f"✅ 已保存合并后的历史数据")
        except Exception as e:
            logger.error(f"保存合并后的历史数据失败：{e}")
            print(f"❌ 保存合并后的历史数据失败：{e}")
    
    logger.info(f"历史数据清洗完成，共处理 {count} 个文件，成功 {success_count} 个，失败 {count - success_count} 个")
    print(f"✅ 历史数据清洗完成，共处理文件：{count}")


def run_clean_realtime(dir_path: str = None, merge_all: bool = True, log_file: str = None):
    """清洗实时数据：扫描 `data/Newraw`（或指定目录）中的 CSV，逐文件调用 `clean_realtime` 并保存结果。
    
    Args:
        dir_path: 原始数据目录路径
        merge_all: 是否合并所有文件的清洗结果为一个文件
        log_file: 日志文件路径（可选）
    """
    try:
        from src.utils.logger import setup_logger
    except Exception as e:
        print(f"⚠️ 无法导入清洗模块：{e}")
        return
    
    # 设置日志
    logger = setup_logger("clean_realtime", log_file=log_file)
    logger.info("开始实时数据清洗操作")
    
    if dir_path is None:
        dir_path = NEWRAW_DATA_DIR
    print(f"📋 开始清洗实时数据，目录：{dir_path}")
    logger.info(f"清洗实时数据，目录：{dir_path}")
    
    count = 0
    success_count = 0
    all_cleaned_data = None
    
    for fname in os.listdir(dir_path):
        logger.info(f"发现文件：{fname}")
        if not fname.lower().endswith('.csv'):
            logger.debug(f"跳过非CSV文件：{fname}")
            continue
        
        fpath = os.path.join(dir_path, fname)
        try:
            df = pd.read_csv(fpath, encoding='utf-8-sig')
            logger.info(f"读取文件成功：{fpath}，共 {len(df)} 行数据")
            
            cleaned_df = _clean_realtime(df)
            count += 1
            success_count += 1
            logger.info(f"清洗文件成功：{fpath}")
            
            # 收集所有清洗后的数据
            if merge_all and cleaned_df is not None and not cleaned_df.empty:
                if all_cleaned_data is None:
                    all_cleaned_data = cleaned_df.copy()
                    logger.info(f"初始化合并数据集，当前数据量：{len(all_cleaned_data)} 行")
                else:
                    prev_count = len(all_cleaned_data)
                    all_cleaned_data = pd.concat([all_cleaned_data, cleaned_df], ignore_index=True)
                    # 去重
                    if "监测站点" in all_cleaned_data.columns:
                        all_cleaned_data = all_cleaned_data.drop_duplicates(subset=[c for c in ["城市", "日期", "小时", "监测站点"] if c in all_cleaned_data.columns])
                        logger.info(f"合并数据：新增 {len(cleaned_df)} 行，合并后共 {len(all_cleaned_data)} 行，去重减少 {prev_count + len(cleaned_df) - len(all_cleaned_data)} 行（按城市+日期+小时+监测站点去重）")
                    else:
                        all_cleaned_data = all_cleaned_data.drop_duplicates(subset=[c for c in ["城市", "日期", "小时"] if c in all_cleaned_data.columns])
                        logger.info(f"合并数据：新增 {len(cleaned_df)} 行，合并后共 {len(all_cleaned_data)} 行，去重减少 {prev_count + len(cleaned_df) - len(all_cleaned_data)} 行（按城市+日期+小时去重）")
                    
        except Exception as e:
            logger.error(f"清洗文件失败：{fpath} -> {e}")
            print(f"❌ 清洗文件失败：{fpath} -> {e}")
    
    # 保存合并后的结果
    if merge_all and all_cleaned_data is not None and not all_cleaned_data.empty:
        logger.info(f"开始合并 {success_count} 个文件的清洗结果，合并后共 {len(all_cleaned_data)} 行数据")
        print(f"📊 正在合并 {success_count} 个文件的清洗结果...")
        
        try:
            _save_processed(all_cleaned_data, "realtime_merged.csv", "realtime_merged")
            logger.info(f"合并后的实时数据已保存，共 {len(all_cleaned_data)} 行")
            print(f"✅ 已保存合并后的实时数据")
        except Exception as e:
            logger.error(f"保存合并后的实时数据失败：{e}")
            print(f"❌ 保存合并后的实时数据失败：{e}")
    
    logger.info(f"实时数据清洗完成，共处理 {count} 个文件，成功 {success_count} 个，失败 {count - success_count} 个")
    print(f"✅ 实时数据清洗完成，共处理文件：{count}")


def run_clean():
    """同时清洗历史与实时数据（先历史后实时）"""
    # 同时清洗历史和实时
    try:
        
        # 使用专用的清洗日志文件
        clean_log_file = os.path.join(BASE_DIR, "data_processing_clean.log")
        logger = setup_logger("clean", log_file=clean_log_file)
        logger.info("开始执行完整的数据清洗操作")
        logger.info("==============================================")
        
        print("🔄 开始执行完整的数据清洗操作...")
        print("==============================================")
        
        # 传递日志文件参数给子函数
        run_clean_history(log_file=clean_log_file)
        print("\n----------------------------------------------")
        run_clean_realtime(log_file=clean_log_file)
        
        logger.info("==============================================")
        logger.info("完整的数据清洗操作执行完成")
        print("\n==============================================")
        print("✅ 完整的数据清洗操作执行完成！")
        print("==============================================")
        
    except Exception as e:
        print(f"❌ 执行清洗操作时发生错误：{e}")
        try:
            logger.error(f"执行清洗操作时发生错误：{e}")
        except:
            pass


__all__ = ["run_clean_history", "run_clean_realtime", "run_clean"]