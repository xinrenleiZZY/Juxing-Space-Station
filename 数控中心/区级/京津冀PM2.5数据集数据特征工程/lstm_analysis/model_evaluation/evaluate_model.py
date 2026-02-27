# 模型评估+预测脚本
"""模型评估主程序：加载模型、评估指标、可视化结果"""
"""模型评估脚本：加载模型→预测→计算指标→保存结果"""
import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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