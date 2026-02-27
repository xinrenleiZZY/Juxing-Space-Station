# LSTM模型定义
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