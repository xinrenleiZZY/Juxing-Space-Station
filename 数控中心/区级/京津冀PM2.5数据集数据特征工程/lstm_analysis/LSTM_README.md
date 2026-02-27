# 京津冀PM2.5日级浓度预测完整可执行解决方案
## 核心需求复述
你需要基于指定的日级数据源`data_preparation/20260119_150028_LstmData.csv`（小时字段为空，仅保留日期维度），构建适配日级时序特性的LSTM预测模型，实现PM2.5浓度精准预测。方案需包含完整的数据预处理、模型构建/训练/评估流程，且严格匹配你指定的文件目录结构，提供可直接运行的代码和清晰的执行说明。

---

## 一、环境准备
### 1.1 依赖库清单（requirements.txt）
```txt
# 核心依赖（适配日级时间序列预测，新手友好）
pandas==2.1.4
numpy==1.26.3
tensorflow==2.15.0  # LSTM模型核心（整合Keras）
scikit-learn==1.3.2 # 数据预处理/评估
matplotlib==3.8.2   # 可视化
seaborn==0.13.1     # 可视化优化
tqdm==4.66.1        # 进度条
joblib==1.3.2       # 保存/加载标准化器
```

### 1.2 依赖安装
```bash
# 1. 创建虚拟环境（推荐）
conda create -n pm25-daily python=3.9 -y
conda activate pm25-daily

# 2. 安装依赖
pip install -r requirements.txt
```

---

## 二、完整文件结构（严格匹配你的要求）
```
lstm_analysis/
├── configs/                # 配置文件目录
│   └── config.py           # 全局配置（路径/参数）
├── data_preparation/       # 数据准备目录
│   └── 20260119_150028_LstmData.csv  # 日级数据源文件
├── data_processing.py      # 数据预处理脚本（核心）
├── model_building/         # 模型构建目录
│   └── lstm_model.py       # LSTM模型定义
├── model_training/         # 模型训练目录
│   └── train_model.py      # 模型训练脚本
├── model_evaluation/       # 模型评估目录
│   └── evaluate_model.py   # 模型评估+预测脚本
├── results/                # 结果保存目录（自动生成）
│   ├── predictions.csv     # 预测结果
│   ├── scaler.pkl          # 标准化器
│   └── trained_model.h5    # 训练好的模型
├── utils/                  # 工具函数目录
│   ├── data_utils.py       # 数据处理工具
│   └── plot_utils.py       # 可视化工具
├── visualization/          # 可视化分析目录
│   └── plot_results.py     # 结果可视化脚本
├── LSTM_README.md          # 项目说明文档
└── requirements.txt        # 依赖库清单
```

---

## 三、全流程可执行代码
### 3.1 全局配置文件（configs/config.py）
```python
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
```

### 3.2 工具函数（utils/data_utils.py）
```python
"""数据处理工具函数：标准化/数据划分/序列构建"""
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from configs.config import SCALER_FILE

def standardize_data(data, fit=True):
    """
    标准化数据（StandardScaler）
    :param data: 待标准化的数据（二维数组）
    :param fit: 是否拟合（训练集fit=True，验证/测试集fit=False）
    :return: 标准化后的数据 + 标准化器
    """
    if fit:
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data)
        # 保存标准化器
        joblib.dump(scaler, SCALER_FILE)
    else:
        # 加载训练好的标准化器
        scaler = joblib.load(SCALER_FILE)
        scaled_data = scaler.transform(data)
    return scaled_data, scaler

def inverse_standardize(data, scaler=None):
    """反标准化数据，恢复原始尺度"""
    if scaler is None:
        scaler = joblib.load(SCALER_FILE)
    return scaler.inverse_transform(data.reshape(-1, 1)).flatten()

def create_sequences(X, y, time_steps):
    """
    构建LSTM输入序列：将一维数据转为(time_steps, features)格式
    :param X: 特征数据（二维数组）
    :param y: 目标数据（一维数组）
    :param time_steps: 时间窗口大小
    :return: 序列特征X_seq, 序列目标y_seq
    """
    X_seq, y_seq = [], []
    for i in range(time_steps, len(X)):
        X_seq.append(X[i-time_steps:i, :])
        y_seq.append(y[i])
    return np.array(X_seq), np.array(y_seq)

def split_train_val_test(data, train_ratio, val_ratio, test_ratio):
    """
    按时间序划分训练/验证/测试集（避免数据泄露）
    :param data: 完整数据（DataFrame）
    :return: train_df, val_df, test_df
    """
    # 按日期排序（关键：时间序列不能随机划分）
    data = data.sort_values("日期")
    total_len = len(data)
    
    # 计算划分索引
    train_end = int(total_len * train_ratio)
    val_end = train_end + int(total_len * val_ratio)
    
    train_df = data.iloc[:train_end]
    val_df = data.iloc[train_end:val_end]
    test_df = data.iloc[val_end:]
    
    print(f"数据集划分完成：")
    print(f"- 训练集：{len(train_df)} 条")
    print(f"- 验证集：{len(val_df)} 条")
    print(f"- 测试集：{len(test_df)} 条")
    
    return train_df, val_df, test_df
```

### 3.3 工具函数（utils/plot_utils.py）
```python
"""可视化工具函数：训练曲线/预测对比/误差分析"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 解决中文字体乱码
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

def plot_training_history(history):
    """绘制模型训练损失曲线"""
    plt.figure(figsize=(12, 4))
    
    # 损失曲线
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='训练损失')
    plt.plot(history.history['val_loss'], label='验证损失')
    plt.title('模型训练损失曲线')
    plt.xlabel('迭代轮数')
    plt.ylabel('均方误差（MSE）')
    plt.legend()
    plt.grid(True)
    
    # 损失下降趋势
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'][10:], label='训练损失（后40轮）')
    plt.plot(history.history['val_loss'][10:], label='验证损失（后40轮）')
    plt.title('损失曲线（后40轮）')
    plt.xlabel('迭代轮数')
    plt.ylabel('均方误差（MSE）')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('visualization/training_history.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("训练损失曲线已保存至 visualization/training_history.png")

def plot_prediction_comparison(y_true, y_pred, dates):
    """绘制预测值vs真实值对比图"""
    # 取前90天数据（便于可视化）
    plot_len = min(90, len(y_true))
    plot_dates = dates[-plot_len:]
    plot_true = y_true[-plot_len:]
    plot_pred = y_pred[-plot_len:]
    
    plt.figure(figsize=(12, 6))
    plt.plot(plot_dates, plot_true, label='真实值', color='#2E86AB', linewidth=2)
    plt.plot(plot_dates, plot_pred, label='预测值', color='#A23B72', linewidth=2, linestyle='--')
    plt.title('PM2.5日级浓度预测值 vs 真实值（前90天）')
    plt.xlabel('日期')
    plt.ylabel('PM2.5浓度（μg/m³）')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('visualization/prediction_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("预测对比图已保存至 visualization/prediction_comparison.png")

def plot_error_analysis(y_true, y_pred):
    """绘制误差分析图"""
    error = y_true - y_pred
    
    plt.figure(figsize=(12, 4))
    
    # 误差分布直方图
    plt.subplot(1, 2, 1)
    sns.histplot(error, bins=30, kde=True, color='#F18F01')
    plt.title('预测误差分布')
    plt.xlabel('误差（μg/m³）')
    plt.ylabel('频次')
    plt.grid(True, alpha=0.3)
    
    # 误差散点图
    plt.subplot(1, 2, 2)
    plt.scatter(y_true, y_pred, alpha=0.6, color='#C73E1D')
    plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'k--', lw=2)
    plt.title('真实值 vs 预测值散点图')
    plt.xlabel('真实值（μg/m³）')
    plt.ylabel('预测值（μg/m³）')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('visualization/error_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("误差分析图已保存至 visualization/error_analysis.png")
```

### 3.4 数据预处理脚本（data_processing.py）
```python
"""
数据预处理核心脚本
功能：加载数据→清洗→特征工程→标准化→构建序列→划分数据集
"""
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
    
    # 2. 数值字段类型转换
    df["AQI"] = pd.to_numeric(df["AQI"], errors='coerce')
    df["PM2.5"] = pd.to_numeric(df["PM2.5"], errors='coerce')
    
    # 3. 缺失值处理：按城市+日期插值（保留时序特性）
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

def preprocess_data():
    """完整预处理流程主函数"""
    # 1. 加载检查
    df = load_and_check_data()
    # 2. 清洗
    df = clean_data(df)
    # 3. 特征工程
    df = feature_engineering(df)
    
    # 4. 按城市合并（简化版：取第一个城市数据，如需多城市可扩展）
    city = df["城市"].unique()[0]
    df_city = df[df["城市"] == city].sort_values("日期").reset_index(drop=True)
    print(f"\n选取城市：{city}，数据量：{len(df_city)}")
    
    # 5. 划分训练/验证/测试集
    train_df, val_df, test_df = split_train_val_test(df_city, TRAIN_RATIO, VAL_RATIO, TEST_RATIO)
    
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
    # 执行预处理
    preprocessed_data = preprocess_data()
    # 保存预处理结果（便于后续训练/评估）
    np.savez("results/preprocessed_data.npz", **preprocessed_data)
    print("\n预处理数据已保存至 results/preprocessed_data.npz")
```

### 3.5 模型构建（model_building/lstm_model.py）
```python
"""LSTM模型定义：适配日级PM2.5预测"""
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from configs.config import (
    TIME_STEPS, FEATURE_COLS, LSTM_UNITS_1, LSTM_UNITS_2,
    DROPOUT_RATE, LEARNING_RATE
)

def build_lstm_model():
    """构建日级LSTM预测模型"""
    # 输入形状：(时间步, 特征数)
    input_shape = (TIME_STEPS, len(FEATURE_COLS))
    
    # 定义模型
    model = Sequential([
        # 第一层LSTM
        LSTM(units=LSTM_UNITS_1, return_sequences=True, input_shape=input_shape),
        Dropout(DROPOUT_RATE),
        # 第二层LSTM
        LSTM(units=LSTM_UNITS_2, return_sequences=False),
        Dropout(DROPOUT_RATE),
        # 输出层（预测PM2.5值）
        Dense(units=1)
    ])
    
    # 编译模型
    optimizer = Adam(learning_rate=LEARNING_RATE)
    model.compile(optimizer=optimizer, loss='mean_squared_error')
    
    # 打印模型结构
    print("=== LSTM模型结构 ===")
    model.summary()
    
    return model

if __name__ == "__main__":
    # 测试模型构建
    model = build_lstm_model()
```

### 3.6 模型训练（model_training/train_model.py）
```python
"""模型训练脚本：加载预处理数据→训练→保存模型"""
import numpy as np
from tensorflow.keras.callbacks import EarlyStopping
from configs.config import BATCH_SIZE, EPOCHS, MODEL_FILE
from model_building.lstm_model import build_lstm_model
from utils.plot_utils import plot_training_history

def train_model():
    """模型训练主函数"""
    print("=== 加载预处理数据 ===")
    # 加载预处理结果
    preprocessed_data = np.load("results/preprocessed_data.npz", allow_pickle=True)
    X_train = preprocessed_data["X_train"]
    y_train = preprocessed_data["y_train"]
    X_val = preprocessed_data["X_val"]
    y_val = preprocessed_data["y_val"]
    
    print("=== 构建LSTM模型 ===")
    model = build_lstm_model()
    
    # 早停机制（防止过拟合）
    early_stopping = EarlyStopping(
        monitor='val_loss',  # 监控验证集损失
        patience=8,          # 8轮无提升则停止
        restore_best_weights=True  # 恢复最佳权重
    )
    
    print("\n=== 开始训练模型 ===")
    # 训练模型
    history = model.fit(
        X_train, y_train,
        batch_size=BATCH_SIZE,
        epochs=EPOCHS,
        validation_data=(X_val, y_val),
        callbacks=[early_stopping],
        verbose=1
    )
    
    # 保存训练好的模型
    model.save(MODEL_FILE)
    print(f"\n模型已保存至：{MODEL_FILE}")
    
    # 绘制训练曲线
    plot_training_history(history)
    
    return model, history

if __name__ == "__main__":
    train_model()
```

### 3.7 模型评估（model_evaluation/evaluate_model.py）
```python
"""模型评估脚本：加载模型→预测→计算指标→保存结果"""
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from configs.config import MODEL_FILE, PREDICTION_FILE
from utils.data_utils import inverse_standardize
from utils.plot_utils import plot_prediction_comparison, plot_error_analysis

def calculate_metrics(y_true, y_pred):
    """计算评估指标：RMSE/MAE/R²"""
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    
    metrics = {
        "RMSE": round(rmse, 2),
        "MAE": round(mae, 2),
        "R²": round(r2, 4)
    }
    return metrics

def evaluate_model():
    """模型评估主函数"""
    print("=== 加载预处理数据和模型 ===")
    # 1. 加载预处理数据
    preprocessed_data = np.load("results/preprocessed_data.npz", allow_pickle=True)
    X_test = preprocessed_data["X_test"]
    y_test_original = preprocessed_data["y_test_original"]
    test_dates = preprocessed_data["test_dates"]
    y_scaler = preprocessed_data["y_scaler"].item()
    
    # 2. 加载训练好的模型
    model = load_model(MODEL_FILE)
    
    print("\n=== 模型预测 ===")
    # 3. 预测
    y_pred_scaled = model.predict(X_test, verbose=0)
    # 4. 反标准化，恢复原始尺度
    y_pred = inverse_standardize(y_pred_scaled, y_scaler)
    
    # 确保预测值和真实值长度一致
    min_len = min(len(y_test_original), len(y_pred))
    y_test_original = y_test_original[:min_len]
    y_pred = y_pred[:min_len]
    test_dates = test_dates[:min_len]
    
    # 5. 计算评估指标
    metrics = calculate_metrics(y_test_original, y_pred)
    print("=== 模型评估指标 ===")
    for metric, value in metrics.items():
        print(f"{metric}: {value}")
    
    # 6. 保存预测结果
    prediction_df = pd.DataFrame({
        "日期": test_dates,
        "PM2.5_真实值": y_test_original,
        "PM2.5_预测值": y_pred,
        "绝对误差": np.abs(y_test_original - y_pred)
    })
    prediction_df.to_csv(PREDICTION_FILE, index=False, encoding='utf-8')
    print(f"\n预测结果已保存至：{PREDICTION_FILE}")
    
    # 7. 可视化预测结果
    plot_prediction_comparison(y_test_original, y_pred, test_dates)
    plot_error_analysis(y_test_original, y_pred)
    
    return metrics

if __name__ == "__main__":
    evaluate_model()
```

### 3.8 可视化脚本（visualization/plot_results.py）
```python
"""一键生成所有可视化结果"""
import sys
sys.path.append(".")  # 添加根目录到路径

from model_evaluation.evaluate_model import evaluate_model

if __name__ == "__main__":
    print("=== 生成可视化结果 ===")
    # 执行评估并生成可视化
    evaluate_model()
    print("\n所有可视化结果已生成至 visualization/ 目录！")
```

### 3.9 项目说明文档（LSTM_README.md）
```markdown
# 京津冀PM2.5日级浓度LSTM预测项目说明

## 1. 项目概述
基于京津冀地区日级空气质量数据（PM2.5、AQI等），构建LSTM时间序列模型，实现对未来PM2.5浓度的精准预测。

## 2. 数据源
- 文件路径：`data_preparation/20260119_150028_LstmData.csv`
- 数据粒度：日级（小时字段为空，已删除）
- 核心字段：城市、日期、AQI、空气质量等级、PM2.5

## 3. 运行步骤
### 3.1 环境准备
```bash
conda create -n pm25-daily python=3.9 -y
conda activate pm25-daily
pip install -r requirements.txt
```

### 3.2 数据预处理
```bash
python data_processing.py
```

### 3.3 模型训练
```bash
python model_training/train_model.py
```

### 3.4 模型评估
```bash
python model_evaluation/evaluate_model.py
```

### 3.5 可视化结果
```bash
python visualization/plot_results.py
```

## 4. 结果说明
- 预测结果：`results/predictions.csv`（包含日期、真实值、预测值、误差）
- 模型文件：`results/trained_model.h5`
- 标准化器：`results/scaler.pkl`
- 可视化图表：
  - `visualization/training_history.png`：训练损失曲线
  - `visualization/prediction_comparison.png`：预测值vs真实值对比
  - `visualization/error_analysis.png`：误差分析图

## 5. 核心参数说明
| 参数 | 说明 | 默认值 |
|------|------|--------|
| TIME_STEPS | 时间窗口（前N天预测下1天） | 7 |
| LSTM_UNITS_1 | 第一层LSTM神经元数 | 64 |
| LSTM_UNITS_2 | 第二层LSTM神经元数 | 32 |
| BATCH_SIZE | 训练批次大小 | 32 |
| EPOCHS | 最大训练轮数 | 50 |

## 6. 扩展建议
1. 多城市支持：修改`data_processing.py`中城市选择逻辑，循环处理多个城市
2. 特征扩展：增加空气质量等级编码、季节特征等
3. 模型优化：调整LSTM层数/神经元数，或尝试GRU/TCN模型
4. 预测窗口扩展：修改TIME_STEPS，实现多步预测（如预测未来3天）
```

---

## 四、运行说明
### 4.1 完整执行流程
```bash
# 1. 进入项目根目录
cd lstm_analysis

# 2. 数据预处理（生成标准化数据和序列）
python data_processing.py

# 3. 模型训练（生成训练好的模型和训练曲线）
python model_training/train_model.py

# 4. 模型评估（生成预测结果和评估指标）
python model_evaluation/evaluate_model.py

# 5. 可视化结果（生成预测对比/误差分析图）
python visualization/plot_results.py
```

### 4.2 结果验证
执行完成后，检查以下文件是否生成：
| 文件路径 | 说明 |
|----------|------|
| `results/preprocessed_data.npz` | 预处理后的序列数据 |
| `results/trained_model.h5` | 训练好的LSTM模型 |
| `results/predictions.csv` | 测试集预测结果 |
| `visualization/training_history.png` | 训练损失曲线 |
| `visualization/prediction_comparison.png` | 预测值vs真实值对比 |
| `visualization/error_analysis.png` | 误差分析图 |

---

## 五、总结
### 核心关键点
1. **数据适配**：针对日级数据特点（小时字段为空），删除无效字段，重点构建日级时间特征（星期、月份）、滞后特征（前1/3天PM2.5）和滚动特征（7天均值）；
2. **时序安全**：按时间序划分训练/验证/测试集，避免随机划分导致的数据泄露；
3. **模型适配**：构建双层LSTM模型，搭配Dropout防止过拟合，早停机制保证训练效率；
4. **结果可解释**：生成完整的评估指标（RMSE/MAE/R²）和可视化图表，直观展示预测效果。

### 关键优化点
1. 若预测精度不足，可调整`configs/config.py`中的`TIME_STEPS`（如改为14天）或LSTM神经元数；
2. 如需支持多城市，修改`data_processing.py`中城市选择逻辑，循环处理每个城市；
3. 若数据量较大，可减小`BATCH_SIZE`或增加`DROPOUT_RATE`防止过拟合。