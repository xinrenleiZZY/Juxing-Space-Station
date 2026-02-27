 # 数据处理工具"""数据处理工具函数：标准化/数据划分/序列构建"""
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