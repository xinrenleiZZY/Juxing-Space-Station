 # 数据预处理脚本（核心）
"""
数据预处理核心脚本
功能：加载数据→清洗→特征工程→标准化→构建序列→划分数据集
"""
import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
import numpy as np
from configs.config import (
    DATA_FILE, FEATURE_COLS, TARGET_COL, TIME_STEPS,
    TRAIN_RATIO, VAL_RATIO, TEST_RATIO
)
from utils.data_utils import standardize_data, create_sequences, split_train_val_test

def load_and_check_data():
    """加载数据并做初步检查"""
    print("=== 1. 加载并检查原始数据 ===")
    # 读取数据
    df = pd.read_csv(DATA_FILE, encoding='utf-8')
    
    # 基本信息检查
    print(f"数据形状：{df.shape}")
    print("\n数据前5行：")
    print(df.head())
    print("\n数据类型：")
    print(df.dtypes)
    print("\n缺失值统计：")
    print(df.isnull().sum())
    
    return df

def clean_data(df):
    """数据清洗：类型转换+缺失值+异常值处理"""
    print("\n=== 2. 数据清洗 ===")
    # 1. 类型转换：日期转为datetime，小时字段为空直接删除
    df = df.drop("小时", axis=1)  # 删除空的小时字段
    df["日期"] = pd.to_datetime(df["日期"], format='%Y-%m-%d')
    
    # 2. 城市名称清洗：去掉"市"字，确保与配置文件一致
    df["城市"] = df["城市"].str.replace("市", "")
    
    # 3. 数值字段类型转换
    df["AQI"] = pd.to_numeric(df["AQI"], errors='coerce')
    df["PM2.5"] = pd.to_numeric(df["PM2.5"], errors='coerce')
    
    # 4. 去除重复值（按城市和日期，保留第一条记录）
    print(f"去重前数据量：{len(df)}")
    df = df.drop_duplicates(subset=["城市", "日期"], keep="first")
    print(f"去重后数据量：{len(df)}")
    
    # 5. 缺失值处理：按城市+日期插值（保留时序特性）
    df = df.sort_values(["城市", "日期"])
    # 数值字段用线性插值填充
    numeric_cols = ["AQI", "PM2.5"]
    for col in numeric_cols:
        df[col] = df.groupby("城市")[col].transform(
            lambda x: x.interpolate(method='linear')
        )
    # 删除剩余少量缺失值
    df = df.dropna(subset=numeric_cols)
    
    # 4. 异常值处理（PM2.5国标范围：0-500 μg/m³）
    df["PM2.5"] = np.clip(df["PM2.5"], 0, 500)
    df["AQI"] = np.clip(df["AQI"], 0, 500)
    
    print(f"清洗后数据形状：{df.shape}")
    print(f"PM2.5范围：{df['PM2.5'].min()} - {df['PM2.5'].max()}")
    
    return df

def feature_engineering(df):
    """特征工程：时间特征+滞后特征+滚动特征"""
    print("\n=== 3. 特征工程 ===")
    # 1. 时间特征提取（日级核心）
    df["year"] = df["日期"].dt.year
    df["month"] = df["日期"].dt.month
    df["day"] = df["日期"].dt.day
    df["weekday"] = df["日期"].dt.weekday  # 0=周一，6=周日
    
    # 2. 滞后特征（前N天的PM2.5值）
    df = df.sort_values(["城市", "日期"])
    df["pm25_lag_1"] = df.groupby("城市")["PM2.5"].shift(1)  # 前1天
    df["pm25_lag_3"] = df.groupby("城市")["PM2.5"].shift(3)  # 前3天
    
    # 3. 滚动统计特征（7天滚动均值）
    df["pm25_roll_7_mean"] = df.groupby("城市")["PM2.5"].rolling(7).mean().reset_index(0, drop=True)
    
    # 删除特征工程产生的缺失值
    df = df.dropna()
    
    # 只保留需要的特征列
    df = df[["城市", "日期"] + FEATURE_COLS]
    
    print(f"特征工程完成，最终列：{df.columns.tolist()}")
    print(f"特征工程后数据形状：{df.shape}")
    
    return df

def preprocess_data(selected_city=None):
    """完整预处理流程主函数
    
    Args:
        selected_city: 选择要处理的城市名称（默认None处理所有城市）
    """
    # 1. 加载检查
    df = load_and_check_data()
    # 2. 清洗
    df = clean_data(df)
    # 3. 特征工程
    df = feature_engineering(df)
    
    # 保存完整预处理数据为CSV
    df.to_csv("results/full_preprocessed_data.csv", index=False, encoding='utf-8')
    print(f"\n完整预处理数据已保存至 results/full_preprocessed_data.csv")
    print(f"数据包含城市：{', '.join(df['城市'].unique())}")
    print(f"总数据量：{len(df)} 条")
    
    # 4. 选择城市数据（可扩展为多城市处理）
    if selected_city is None:
        # 默认取第一个城市数据（保持与原有逻辑兼容）
        selected_city = df["城市"].unique()[0]
    
    df_city = df[df["城市"] == selected_city].sort_values("日期").reset_index(drop=True)
    print(f"\n选取城市：{selected_city}，数据量：{len(df_city)}")
    
    # 5. 划分训练/验证/测试集
    train_df, val_df, test_df = split_train_val_test(df_city, TRAIN_RATIO, VAL_RATIO, TEST_RATIO)
    
    # 保存划分后的数据集为CSV
    train_df.to_csv("results/train_data.csv", index=False, encoding='utf-8')
    val_df.to_csv("results/val_data.csv", index=False, encoding='utf-8')
    test_df.to_csv("results/test_data.csv", index=False, encoding='utf-8')
    print(f"\n数据集已保存至 results/ 目录：")
    print(f"- 训练集：{len(train_df)} 条")
    print(f"- 验证集：{len(val_df)} 条")
    print(f"- 测试集：{len(test_df)} 条")
    
    # 6. 标准化（仅标准化特征列，目标列单独处理）
    X_train = train_df[FEATURE_COLS].values
    X_val = val_df[FEATURE_COLS].values
    X_test = test_df[FEATURE_COLS].values
    
    y_train = train_df[TARGET_COL].values
    y_val = val_df[TARGET_COL].values
    y_test = test_df[TARGET_COL].values
    
    # 标准化特征
    X_train_scaled, scaler = standardize_data(X_train, fit=True)
    X_val_scaled, _ = standardize_data(X_val, fit=False)
    X_test_scaled, _ = standardize_data(X_test, fit=False)
    
    # 标准化目标值（单独标准化，便于后续反转换）
    y_train_scaled, y_scaler = standardize_data(y_train.reshape(-1, 1), fit=True)
    y_val_scaled, _ = standardize_data(y_val.reshape(-1, 1), fit=False)
    y_test_scaled, _ = standardize_data(y_test.reshape(-1, 1), fit=False)
    
    # 7. 构建LSTM序列
    X_train_seq, y_train_seq = create_sequences(X_train_scaled, y_train_scaled, TIME_STEPS)
    X_val_seq, y_val_seq = create_sequences(X_val_scaled, y_val_scaled, TIME_STEPS)
    X_test_seq, y_test_seq = create_sequences(X_test_scaled, y_test_scaled, TIME_STEPS)
    
    # 保存测试集日期（用于可视化）
    test_dates = test_df["日期"].iloc[TIME_STEPS:].reset_index(drop=True)
    
    print("\n=== 预处理完成 ===")
    print(f"训练序列形状：X={X_train_seq.shape}, y={y_train_seq.shape}")
    print(f"验证序列形状：X={X_val_seq.shape}, y={y_val_seq.shape}")
    print(f"测试序列形状：X={X_test_seq.shape}, y={y_test_seq.shape}")
    
    # 返回预处理结果
    return {
        "X_train": X_train_seq, "y_train": y_train_seq,
        "X_val": X_val_seq, "y_val": y_val_seq,
        "X_test": X_test_seq, "y_test": y_test_seq,
        "y_test_original": y_test,  # 原始测试集目标值
        "test_dates": test_dates,   # 测试集日期
        "y_scaler": y_scaler        # 目标值标准化器
    }

if __name__ == "__main__":
    import argparse
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="数据预处理脚本")
    parser.add_argument("--city", type=str, default=None, help="选择要处理的城市名称")
    args = parser.parse_args()
    
    # 执行预处理
    preprocessed_data = preprocess_data(selected_city=args.city)
    
    # 保存预处理结果（便于后续训练/评估）
    np.savez("results/preprocessed_data.npz", **preprocessed_data)
    print("\n预处理数据已保存至 results/preprocessed_data.npz")
    
    # 显示使用说明
    print("\n使用说明：")
    print("- 处理特定城市数据：python data_processing.py --city 北京")
    print("- 处理所有城市数据：python data_processing.py")
    print("- 查看完整预处理数据：检查 results/full_preprocessed_data.csv")