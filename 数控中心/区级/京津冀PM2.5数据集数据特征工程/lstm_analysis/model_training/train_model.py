# 模型训练脚本
"""模型训练主程序：加载数据、构建模型、训练并保存"""
"""模型训练脚本：加载预处理数据→训练→保存模型"""
import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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