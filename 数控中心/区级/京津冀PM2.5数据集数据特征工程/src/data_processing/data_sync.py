import os
import time
import pandas as pd
import logging
from config.settings import PROCESSED_DATA_DIR
from src.utils.logger import setup_logger


def data_sync():
    """同步data/processed的CSV文件到lstm_analysis/data_preparation
    
    功能：
    - 读取data/processed目录下的所有CSV文件
    - 合并这些CSV文件
    - 保存为时间戳_LstmData.csv格式到lstm_analysis/data_preparation目录
    """
    logger = setup_logger("data_sync")
    logger.info("开始执行数据同步操作")
    
    print("🔄 开始执行数据同步操作...")
    print("==============================================")
    
    try:
        # 获取processed目录下的所有CSV文件
        processed_dir = PROCESSED_DATA_DIR
        csv_files = [f for f in os.listdir(processed_dir) if f.lower().endswith('.csv')]
        
        if not csv_files:
            logger.warning("没有找到需要同步的CSV文件")
            print("⚠️  没有找到需要同步的CSV文件")
            return
        
        logger.info(f"发现 {len(csv_files)} 个CSV文件需要同步")
        print(f"📁 发现 {len(csv_files)} 个CSV文件需要同步")
        
        # 合并所有CSV文件
        all_data = []
        for file_name in csv_files:
            file_path = os.path.join(processed_dir, file_name)
            try:
                logger.info(f"读取文件：{file_path}")
                df = pd.read_csv(file_path, encoding='utf-8-sig')
                all_data.append(df)
                print(f"✅ 读取成功：{file_name}")
            except Exception as e:
                logger.error(f"读取文件失败：{file_path} -> {e}")
                print(f"❌ 读取文件失败：{file_name} -> {e}")
        
        if not all_data:
            logger.error("没有成功读取任何CSV文件")
            print("❌ 没有成功读取任何CSV文件")
            return
        
        # 合并数据
        merged_data = pd.concat(all_data, ignore_index=True)
        logger.info(f"合并完成，共 {len(merged_data)} 行数据")
        print(f"📊 合并完成，共 {len(merged_data)} 行数据")
        
        # 创建输出路径（项目根目录下的lstm_analysis）
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        output_dir = os.path.join(project_root, "lstm_analysis", "data_preparation")
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成时间戳文件名
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_file = f"{timestamp}_LstmData.csv"
        output_path = os.path.join(output_dir, output_file)
        
        # 保存文件
        merged_data.to_csv(output_path, index=False, encoding='utf-8-sig')
        logger.info(f"数据已保存到：{output_path}")
        print(f"✅ 数据已保存到：{output_path}")
        
        logger.info("数据同步操作完成")
        print("==============================================")
        print("✅ 数据同步操作完成！")
        print("==============================================")
        
    except Exception as e:
        logger.error(f"数据同步操作失败：{e}")
        print(f"❌ 数据同步操作失败：{e}")


__all__ = ["data_sync"]