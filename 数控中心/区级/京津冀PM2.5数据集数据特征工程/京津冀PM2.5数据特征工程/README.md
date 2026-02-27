## 京津冀PM2.5数据特征工程

## 项目概述

本项目对2015-2025年京津冀地区每日PM2.5数据进行创造性加工处理，生成符合数据知识产权登记要求的高价值数据集。通过系统性的特征工程，将原始浓度数据转化为包含时间模式、空间关系、污染事件、政策影响和健康风险等多维度信息的知识产品。

## 项目结构


```
京津冀PM2.5数据特征工程/
├── config/
│   └── settings.py          # 配置文件
├── data/
│   ├── raw/                 # 原始数据（从原项目复制）
│   ├── processed/           # 处理后的数据
│   ├── features/            # 特征工程结果
│   └── external/            # 外部数据（气象数据、政策时间线等）
├── src/
│   ├── data_preprocessing.py      # 数据预处理模块
│   ├── feature_engineering.py     # 特征工程
│   ├── spatial_analysis.py        # 空间分析模块
│   ├── policy_analysis.py         # 政策分析模块
│   └── utils/
│       ├── __init__.py
│       ├── data_loader.py         # 数据加载工具
│       └── visualizer.py          # 可视化工具
├── notebooks/               # Jupyter notebooks
│   ├── 01_data_exploration.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_analysis_and_visualization.ipynb
├── requirements.txt         # 依赖包
├── README.md                # 项目说明
└── run_pipeline.py          # 主运行脚本
```

## 安装与使用

### 1. 环境配置

```bash
# 克隆项目
git clone <repository-url>
cd 京津冀PM2.5数据特征工程

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

```
2. 准备数据
将您的原始PM2.5数据（CSV格式）放置在 data/raw/ 目录下，命名为 pm25_raw_data.csv。

数据应至少包含以下列：

date: 日期（YYYY-MM-DD格式）

city: 城市名称

pm25: PM2.5浓度值（μg/m³）

3. 运行流水线
# 运行完整的数据处理和特征工程流水线

python run_pipeline.py

流水线将执行以下步骤：
数据预处理（清洗、插补、质量控制）
特征工程（时间特征、空间特征、污染事件识别等）
结果保存和文档生成

4. 查看结果
处理完成后，可以在以下位置查看结果：

data/processed/pm25_processed.csv - 清洗后的基础数据
data/features/pm25_with_features.csv - 包含所有特征的数据集
data/features/feature_documentation.md - 特征说明文档
data/features/policy_effects_analysis.csv - 政策效果分析

创造性加工说明

时间特征
滑动平均（7天、30天）
趋势分析（30天趋势斜率）
同比变化计算
季节性和周期性分析
污染事件识别
自动识别持续污染过程
事件持续时间、峰值强度计算
严重性综合指数
空间特征
区域相对排名
偏离区域均值程度
热点区域识别
政策与健康特征
政策时期标签
重大活动标志
AQI等级分类
累计暴露量和超标负担

扩展与定制
添加新特征
在 src/feature_engineering.py 中添加新的特征工程方法，或修改现有方法。

调整参数
在 config/settings.py 中修改城市列表、政策时间线、阈值参数等。

可视化分析
使用 notebooks/ 中的Jupyter笔记本进行数据分析和可视化。

许可证
本项目遵循MIT许可证。数据使用请遵守相关法律法规和数据提供方的规定。

text
### **8. Jupyter笔记本示例 (notebooks/02_feature_engineering.ipynb)**

由于Jupyter笔记本内容较长，这里提供一个简化的模板：

```python
# notebooks/02_feature_engineering.ipynb
# 特征工程分析与可视化笔记本

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# 添加项目根目录到路径
sys.path.append('..')

# 加载特征工程后的数据
features_path = Path('../data/features/pm25_with_features.csv')
df = pd.read_csv(features_path, parse_dates=['date'])

print("数据集概览:")
print(f"记录数: {len(df):,}")
print(f"特征数: {len(df.columns)}")
print(f"时间范围: {df['date'].min().date()} 到 {df['date'].max().date()}")
print(f"城市数量: {df['city'].nunique()}")

# 1. 时间特征分析
plt.figure(figsize=(15, 10))

# 北京PM2.5浓度时间序列
plt.subplot(2, 2, 1)
bj_data = df[df['city'] == '北京市'].sort_values('date')
plt.plot(bj_data['date'], bj_data['pm25'], alpha=0.7, label='日浓度')
plt.plot(bj_data['date'], bj_data['rolling_avg_30d'], 'r-', linewidth=2, label='30日滑动平均')
plt.title('北京市PM2.5浓度时间序列')
plt.xlabel('日期')
plt.ylabel('PM2.5浓度 (μg/m³)')
plt.legend()
plt.grid(True, alpha=0.3)

# 2. 污染事件分析
plt.subplot(2, 2, 2)
event_cities = df[~df['pollution_event_id'].isna()]['city'].value_counts()
event_cities.plot(kind='bar')
plt.title('各城市污染事件数量')
plt.xlabel('城市')
plt.ylabel('污染事件数')
plt.xticks(rotation=45)

# 3. 空间特征分析
plt.subplot(2, 2, 3)
# 选取最近一天的数据
latest_date = df['date'].max()
latest_data = df[df['date'] == latest_date]

# 按偏离程度排序
sorted_data = latest_data.sort_values('deviation_from_regional_avg', ascending=False)
plt.bar(range(len(sorted_data)), sorted_data['deviation_from_regional_avg'])
plt.xticks(range(len(sorted_data)), sorted_data['city'], rotation=90)
plt.title(f'{latest_date.date()} 各城市偏离区域均值程度')
plt.xlabel('城市')
plt.ylabel('偏离区域均值 (%)')

# 4. AQI等级分布
plt.subplot(2, 2, 4)
aqi_dist = df['aqi_category'].value_counts()
plt.pie(aqi_dist.values, labels=aqi_dist.index, autopct='%1.1f%%')
plt.title('整体AQI等级分布')

plt.tight_layout()
plt.show()

# 5. 政策效果分析
policy_effects_path = Path('../data/features/policy_effects_analysis.csv')
policy_effects = pd.read_csv(policy_effects_path)

print("\n政策效果分析:")
print(policy_effects.to_string(index=False))

# 6. 特征相关性分析（示例：选取部分特征）
selected_features = ['pm25', 'rolling_avg_7d', 'rolling_avg_30d', 
                     'trend_30d', 'deviation_from_regional_avg',
                     'cumulative_exposure_30d', 'exceedance_burden_365d']

correlation_data = df[selected_features].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_data, annot=True, cmap='coolwarm', center=0,
            square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
plt.title('特征相关性热力图')
plt.tight_layout()
plt.show()

使用流程
准备原始数据：
bash
# 将您的原始数据复制到 data/raw/pm25_raw_data.csv
cp 您的原始数据.csv data/raw/pm25_raw_data.csv
运行完整流水线：

bash
python run_pipeline.py
查看和分析结果：

查看处理日志和统计信息

在 data/features/ 目录下查看生成的数据集

使用Jupyter笔记本进行可视化分析

准备数据知识产权登记材料：

使用 data/features/feature_documentation.md 作为数据处理说明

使用特征工程后的数据集作为申请材料

参考处理流程说明创造性加工过程

这个完整的项目结构为您提供了：

模块化代码：每个功能独立，易于维护和扩展

完整文档：包含特征说明和处理流程

可复现性：确保每次处理结果一致

可追溯性：记录每个数据处理步骤
## 数据预处理

1. 将原始数据复制到 `data/raw/` 目录
2. 运行数据预处理脚本：

```python
from src.data_preprocessing import load_data, clean_data, merge_historical_data

# 加载数据
df = load_data('data/raw/your_data.csv')

# 清洗数据
df_clean = clean_data(df)

# 合并历史数据
df_merged = merge_historical_data('data/raw/')
```
