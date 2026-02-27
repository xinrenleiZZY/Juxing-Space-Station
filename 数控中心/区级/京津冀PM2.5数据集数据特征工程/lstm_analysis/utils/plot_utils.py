# 可视化工具
"""可视化工具函数：训练曲线/预测对比/误差分析"""
import matplotlib
matplotlib.use('Agg')  # 设置非交互式后端
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