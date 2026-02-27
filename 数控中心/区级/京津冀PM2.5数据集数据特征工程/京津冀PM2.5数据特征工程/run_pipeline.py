# run_pipeline.py
#!/usr/bin/env python3
"""
京津冀PM2.5数据特征工程主运行脚本
"""

import sys
import time
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent))

from src.data_preprocessing import DataPreprocessor
from src.feature_engineering import FeatureEngineer

def run_full_pipeline():
    """
    运行完整的数据处理与特征工程流水线
    """
    print("=" * 60)
    print("京津冀PM2.5数据特征工程流水线")
    print("=" * 60)
    
    start_time = time.time()
    
    # 第一阶段：数据预处理
    print("\n[阶段1] 数据预处理")
    print("-" * 40)
    
    preprocessor = DataPreprocessor()
    processed_data = preprocessor.run_pipeline(save_output=True)
    
    if processed_data is None:
        print("数据预处理失败，退出流程")
        return
    
    # 第二阶段：特征工程
    print("\n[阶段2] 特征工程")
    print("-" * 40)
    
    engineer = FeatureEngineer()
    featured_data = engineer.run_pipeline(save_output=True)
    
    if featured_data is None:
        print("特征工程失败，退出流程")
        return
    
    # 计算总耗时
    end_time = time.time()
    total_time = end_time - start_time
    
    print("\n" + "=" * 60)
    print("流水线执行完成!")
    print(f"总耗时: {total_time:.2f} 秒")
    
    # 输出结果摘要
    print("\n结果摘要:")
    print(f"- 处理后的数据保存至: data/processed/pm25_processed.csv")
    print(f"- 特征工程结果保存至: data/features/pm25_with_features.csv")
    print(f"- 特征说明文档保存至: data/features/feature_documentation.md")
    print(f"- 政策效果分析保存至: data/features/policy_effects_analysis.csv")
    
    # 显示最终数据集信息
    if featured_data is not None:
        print(f"\n最终数据集信息:")
        print(f"  记录数: {len(featured_data):,}")
        print(f"  特征数: {len(featured_data.columns)}")
        print(f"  时间范围: {featured_data['date'].min().date()} 到 {featured_data['date'].max().date()}")
        print(f"  城市数量: {featured_data['city'].nunique()}")
        
        # 显示前几个特征名
        print(f"\n部分特征示例:")
        features_list = list(featured_data.columns)[:15]
        for i, feat in enumerate(features_list, 1):
            print(f"  {i:2d}. {feat}")
        
        if len(featured_data.columns) > 15:
            print(f"  ... 还有 {len(featured_data.columns) - 15} 个特征")

if __name__ == "__main__":
    run_full_pipeline()