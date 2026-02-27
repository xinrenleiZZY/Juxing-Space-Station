# PM2.5预测可视化大屏
# 基于Streamlit构建的交互式数据分析与模型可视化平台

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.models import load_model
import joblib
import os

# 设置中文字体
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

# 设置页面配置
st.set_page_config(
    page_title="PM2.5日级预测可视化大屏",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 创建侧边栏
st.sidebar.title("🎛️ 控制面板")

# 加载数据
@st.cache_data

def load_data():
    """加载所有数据"""
    # 加载完整预处理数据
    full_data = pd.read_csv("results/full_preprocessed_data.csv")
    full_data["日期"] = pd.to_datetime(full_data["日期"])
    
    # 加载预测结果
    predictions = pd.read_csv("results/predictions.csv")
    predictions["日期"] = pd.to_datetime(predictions["日期"])
    
    return full_data, predictions

# 加载模型
@st.cache_resource

def load_trained_model():
    """加载训练好的模型"""
    if os.path.exists("results/trained_model.h5"):
        model = load_model("results/trained_model.h5")
        return model
    else:
        return None

# 加载标准化器
@st.cache_resource

def load_scaler():
    """加载标准化器"""
    if os.path.exists("results/scaler.pkl"):
        scaler = joblib.load("results/scaler.pkl")
        return scaler
    else:
        return None

# 主页面标题
st.title("📊 PM2.5日级预测可视化大屏")

# 加载数据
full_data, predictions = load_data()
model = load_trained_model()
scaler = load_scaler()

# 城市选择
cities = full_data["城市"].unique().tolist()
selected_city = st.sidebar.selectbox(
    "选择城市",
    cities,
    index=0
)

# 时间范围选择
min_date = full_data["日期"].min()
max_date = full_data["日期"].max()

date_range = st.sidebar.date_input(
    "选择时间范围",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# 筛选数据
filtered_data = full_data[(
    (full_data["城市"] == selected_city) & 
    (full_data["日期"] >= pd.to_datetime(date_range[0])) & 
    (full_data["日期"] <= pd.to_datetime(date_range[1]))
)]

filtered_predictions = predictions[(
    (predictions["日期"] >= pd.to_datetime(date_range[0])) & 
    (predictions["日期"] <= pd.to_datetime(date_range[1]))
)]

# 显示数据概览卡片
st.subheader("📈 数据概览")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("总数据量", f"{len(full_data):,} 条")

with col2:
    st.metric("覆盖城市数", f"{len(cities)} 个")

with col3:
    st.metric("时间跨度", f"{min_date.strftime('%Y-%m-%d')} 至 {max_date.strftime('%Y-%m-%d')}")

with col4:
    st.metric("所选城市数据量", f"{len(filtered_data):,} 条")

# 数据质量分析
st.subheader("🔍 数据质量分析")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 缺失值分析")
    missing_values = filtered_data.isnull().sum()
    missing_df = pd.DataFrame({
        "特征": missing_values.index,
        "缺失值数量": missing_values.values,
        "缺失值比例": (missing_values.values / len(filtered_data) * 100).round(2)
    })
    st.dataframe(missing_df, use_container_width=True)

with col2:
    st.markdown("### 数据分布概览")
    desc_stats = filtered_data[["PM2.5", "AQI"]].describe().T
    st.dataframe(desc_stats[["mean", "std", "min", "25%", "50%", "75%", "max"]], use_container_width=True)

# 特征工程可视化
st.subheader("⚙️ 特征工程可视化")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### PM2.5滞后特征")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.scatterplot(x=filtered_data["pm25_lag_1"], y=filtered_data["PM2.5"], ax=ax, alpha=0.6, color="#2E86AB")
    ax.set_title(f"{selected_city} - 前1天PM2.5与当天PM2.5关系")
    ax.set_xlabel("前1天PM2.5浓度 (μg/m³)")
    ax.set_ylabel("当天PM2.5浓度 (μg/m³)")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

with col2:
    st.markdown("### PM2.5滚动特征")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.scatterplot(x=filtered_data["pm25_roll_7_mean"], y=filtered_data["PM2.5"], ax=ax, alpha=0.6, color="#A23B72")
    ax.set_title(f"{selected_city} - 7天滚动平均与当天PM2.5关系")
    ax.set_xlabel("7天滚动平均PM2.5浓度 (μg/m³)")
    ax.set_ylabel("当天PM2.5浓度 (μg/m³)")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

# 月度趋势分析
st.subheader("📅 月度趋势分析")
# 先添加年份和月份列
monthly_data = filtered_data.copy()
monthly_data["年份"] = monthly_data["日期"].dt.year
monthly_data["月份"] = monthly_data["日期"].dt.month
# 然后按年份和月份分组
monthly_data = monthly_data.groupby(["年份", "月份"])["PM2.5"].mean().reset_index()
# 格式化月份列
monthly_data["月份"] = monthly_data["年份"].astype(str) + "-" + monthly_data["月份"].astype(str).str.zfill(2)

fig, ax = plt.subplots(figsize=(15, 6))
sns.lineplot(x="月份", y="PM2.5", data=monthly_data, ax=ax, marker="o", color="#F18F01", linewidth=2)
ax.set_title(f"{selected_city} - PM2.5月度平均趋势")
ax.set_xlabel("月份")
ax.set_ylabel("PM2.5平均浓度 (μg/m³)")
ax.tick_params(axis="x", rotation=45)
ax.grid(True, alpha=0.3)
st.pyplot(fig)

# 模型性能展示
st.subheader("🤖 模型性能展示")
if model:
    # 模型架构
    st.markdown("### 模型架构")
    model_summary = []
    model.summary(print_fn=lambda x: model_summary.append(x))
    model_summary = "\n".join(model_summary)
    st.text(model_summary)
    
    # 评估指标
    st.markdown("### 评估指标")
    # 计算评估指标
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    
    if len(filtered_predictions) > 0:
        y_true = filtered_predictions["PM2.5_真实值"].values
        y_pred = filtered_predictions["PM2.5_预测值"].values
        
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        
        metrics_df = pd.DataFrame({
            "指标": ["RMSE", "MAE", "R²"],
            "值": [round(rmse, 2), round(mae, 2), round(r2, 4)],
            "说明": ["均方根误差", "平均绝对误差", "决定系数"]
        })
        
        st.dataframe(metrics_df, use_container_width=True)
    else:
        st.warning("当前时间范围内没有预测数据")
else:
    st.warning("模型文件不存在，请先运行模型训练")

# 预测结果对比
st.subheader("🎯 预测结果对比")
if len(filtered_predictions) > 0:
    # 选择显示天数
    display_days = st.sidebar.slider("选择显示天数", 7, 90, 30)
    
    # 取最近的display_days天数据
    recent_predictions = filtered_predictions.tail(display_days)
    
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.plot(recent_predictions["日期"], recent_predictions["PM2.5_真实值"], label="真实值", color="#2E86AB", linewidth=2)
    ax.plot(recent_predictions["日期"], recent_predictions["PM2.5_预测值"], label="预测值", color="#A23B72", linewidth=2, linestyle="--")
    ax.set_title(f"{selected_city} - PM2.5预测值与真实值对比 ({display_days}天)")
    ax.set_xlabel("日期")
    ax.set_ylabel("PM2.5浓度 (μg/m³)")
    ax.tick_params(axis="x", rotation=45)
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
else:
    st.warning("当前时间范围内没有预测数据")

# 误差分析
st.subheader("📊 误差分析")
if len(filtered_predictions) > 0:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 误差分布")
        error = filtered_predictions["PM2.5_真实值"] - filtered_predictions["PM2.5_预测值"]
        
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(error, bins=30, kde=True, ax=ax, color="#F18F01")
        ax.set_title(f"{selected_city} - 预测误差分布")
        ax.set_xlabel("误差 (μg/m³)")
        ax.set_ylabel("频次")
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
    
    with col2:
        st.markdown("### 真实值与预测值散点图")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.scatterplot(x=filtered_predictions["PM2.5_真实值"], y=filtered_predictions["PM2.5_预测值"], ax=ax, alpha=0.6, color="#C73E1D")
        
        # 添加对角线
        min_val = min(filtered_predictions["PM2.5_真实值"].min(), filtered_predictions["PM2.5_预测值"].min())
        max_val = max(filtered_predictions["PM2.5_真实值"].max(), filtered_predictions["PM2.5_预测值"].max())
        ax.plot([min_val, max_val], [min_val, max_val], "k--", lw=2)
        
        ax.set_title(f"{selected_city} - 真实值 vs 预测值")
        ax.set_xlabel("真实值 (μg/m³)")
        ax.set_ylabel("预测值 (μg/m³)")
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
else:
    st.warning("当前时间范围内没有预测数据")

# 特征相关性分析
st.subheader("🔗 特征相关性分析")
features = ["PM2.5", "AQI", "pm25_lag_1", "pm25_lag_3", "pm25_roll_7_mean"]
corr_matrix = filtered_data[features].corr()

fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=ax, fmt=".2f", square=True, cbar_kws={"shrink": 0.8})
ax.set_title(f"{selected_city} - 特征相关性矩阵")
st.pyplot(fig)

# 页脚
st.markdown("---")
st.markdown("### 📝 说明")
st.markdown("1. 本大屏基于LSTM模型实现PM2.5日级预测")
st.markdown("2. 数据涵盖13个城市的历史PM2.5监测数据")
st.markdown("3. 特征工程包含时间特征、滞后特征和滚动特征")
st.markdown("4. 可通过控制面板选择不同城市和时间范围进行分析")
st.markdown("5. 模型性能指标实时计算，可视化展示预测效果")

# 运行说明
st.sidebar.markdown("---")
st.sidebar.markdown("### 🚀 运行说明")
st.sidebar.markdown("1. 选择要分析的城市")
st.sidebar.markdown("2. 设置时间范围")
st.sidebar.markdown("3. 调整显示天数")
st.sidebar.markdown("4. 浏览各模块的可视化结果")

# 技术栈
st.sidebar.markdown("---")
st.sidebar.markdown("### 🛠️ 技术栈")
st.sidebar.markdown("- Python 3.8+")
st.sidebar.markdown("- Streamlit")
st.sidebar.markdown("- TensorFlow/Keras")
st.sidebar.markdown("- Matplotlib/Seaborn")
st.sidebar.markdown("- Pandas/Numpy")
