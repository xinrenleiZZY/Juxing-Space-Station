"""全局配置文件：统一管理路径和模型参数"""
import os
from pathlib import Path

# 根目录
ROOT_DIR = Path(__file__).parent.parent

# ========== 路径配置 ==========
# 数据源路径
DATA_FILE = ROOT_DIR / "data_preparation/20260119_150028_LstmData.csv"
# 结果保存路径
RESULTS_DIR = ROOT_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)  # 自动创建目录
PREDICTION_FILE = RESULTS_DIR / "predictions.csv"
SCALER_FILE = RESULTS_DIR / "scaler.pkl"
MODEL_FILE = RESULTS_DIR / "trained_model.h5"

# ========== 数据预处理参数 ==========
# 目标列（预测值）
TARGET_COL = "PM2.5"
# 特征列（用于预测的特征）
FEATURE_COLS = ["AQI", "PM2.5", "year", "month", "day", "weekday", 
                "pm25_lag_1", "pm25_lag_3", "pm25_roll_7_mean"]
# 时间窗口：用前N天数据预测下1天（日级核心参数）
TIME_STEPS = 7  # 前7天 → 预测第8天
# 数据集划分比例
TRAIN_RATIO = 0.7   # 训练集70%
VAL_RATIO = 0.15    # 验证集15%
TEST_RATIO = 0.15   # 测试集15%

# ========== LSTM模型参数 ==========
LSTM_UNITS_1 = 64   # 第一层LSTM神经元数
LSTM_UNITS_2 = 32   # 第二层LSTM神经元数
DROPOUT_RATE = 0.2  # Dropout防止过拟合
BATCH_SIZE = 32     # 批次大小
EPOCHS = 50         # 训练轮数
LEARNING_RATE = 0.001  # 学习率