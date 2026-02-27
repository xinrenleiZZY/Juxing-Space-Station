# PM2.5日级预测可视化大屏

## 📊 项目概述

本项目是一个基于LSTM（长短期记忆网络）的PM2.5日级浓度预测系统，包含完整的数据预处理、模型训练、评估和可视化功能。通过Streamlit构建的交互式可视化大屏，用户可以直观地分析PM2.5数据特征、评估模型性能和查看预测结果。

## 🚀 快速开始

### 1. 环境要求

- Python 3.8+
- 主要依赖包：
  - streamlit
  - pandas
  - numpy
  - matplotlib
  - seaborn
  - tensorflow
  - scikit-learn
  - joblib

### 2. 安装依赖

```bash
# 进入项目目录
cd lstm_analysis

# 安装所有依赖
pip install -r requirements.txt
```

### 3. 运行应用

本项目提供两种运行方式：

#### 方式一：使用主入口文件（推荐）

```bash
python main.py
```

#### 方式二：直接运行Streamlit

```bash
streamlit run visualization_dashboard.py
```

### 4. 访问应用

应用启动后，将在浏览器中自动打开，或通过以下地址访问：
- **本地访问**：http://localhost:8501
- **网络访问**：http://192.168.1.135:8501（根据实际网络配置）

## 🎯 功能模块

### 1. 数据概览
- 显示总数据量、覆盖城市数、时间跨度
- 实时更新所选城市的数据统计信息

### 2. 数据质量分析
- 缺失值分析：展示各特征的缺失值数量和比例
- 数据分布概览：提供PM2.5和AQI的统计信息（均值、标准差、最值等）

### 3. 特征工程可视化
- **滞后特征分析**：展示前1天PM2.5与当天PM2.5的关系
- **滚动特征分析**：展示7天滚动平均与当天PM2.5的关系

### 4. 月度趋势分析
- 展示所选城市PM2.5的月度平均趋势变化
- 直观呈现季节性波动规律

### 5. 模型性能展示
- **模型架构**：详细展示LSTM模型的层结构和参数配置
- **评估指标**：计算并显示关键性能指标（RMSE、MAE、R²）

### 6. 预测结果对比
- 可视化展示预测值与真实值的时间序列对比
- 支持自定义显示天数（7-90天）

### 7. 误差分析
- **误差分布直方图**：展示预测误差的频率分布
- **真实值vs预测值散点图**：评估预测准确性

### 8. 特征相关性分析
- 热力图展示所有特征之间的相关性
- 帮助理解特征间的相互关系

## 🎛️ 使用指南

### 1. 控制面板操作

- **城市选择**：在左侧侧边栏选择要分析的城市（支持13个城市）
- **时间范围选择**：可自定义分析时间段
- **显示天数调整**：在预测结果对比模块中，可设置显示天数（7-90天）

### 2. 数据浏览

1. 在控制面板中选择城市
2. 设置时间范围
3. 浏览各模块的可视化结果
4. 可点击图表进行放大查看细节
5. 可将感兴趣的数据表格导出为CSV文件

### 3. 模型分析

- 查看模型架构了解LSTM网络结构
- 通过评估指标判断模型性能
- 分析预测结果与真实值的差异
- 查看误差分布了解预测的稳定性

## 📁 项目结构

```
lstm_analysis/
├── data_processing/            # 数据预处理模块
│   └── data_processing.py      # 数据预处理脚本
├── model_building/             # 模型构建模块
│   └── lstm_model.py           # LSTM模型定义
├── model_training/             # 模型训练模块
│   └── train_model.py          # 模型训练脚本
├── model_evaluation/           # 模型评估模块
│   └── evaluate_model.py       # 模型评估脚本
├── utils/                      # 工具函数
│   ├── data_utils.py           # 数据处理工具
│   └── plot_utils.py           # 可视化工具
├── configs/                    # 配置文件
│   └── config.py               # 项目配置
├── results/                    # 结果文件
│   ├── full_preprocessed_data.csv  # 完整预处理数据
│   ├── predictions.csv         # 预测结果
│   ├── trained_model.h5        # 训练好的模型
│   └── scaler.pkl              # 标准化器
├── visualization/              # 可视化结果
├── main.py                     # 项目主入口
├── visualization_dashboard.py  # 可视化大屏
├── requirements.txt            # 依赖列表
└── README.md                   # 项目说明
```

## 🛠️ 技术栈

- **数据处理**：Pandas, NumPy
- **模型构建**：TensorFlow/Keras
- **特征工程**：时间特征、滞后特征、滚动特征
- **可视化**：Matplotlib, Seaborn, Streamlit
- **模型评估**：Scikit-learn
- **部署**：Streamlit

## 💡 注意事项

1. **数据更新**：若需要更新数据，可将新数据放入`data_processing/`目录下，然后重新运行数据预处理脚本

2. **模型重新训练**：
   ```bash
   python model_training/train_model.py
   ```

3. **性能优化**：
   - 可调整`configs/config.py`中的参数优化模型性能
   - 当前模型R²为负值，可通过增加特征数量、调整LSTM层数等方式改进

4. **浏览器兼容性**：推荐使用Chrome、Firefox等现代浏览器

## 📝 常见问题

### Q: 应用启动失败怎么办？
A: 请检查是否已安装所有依赖，可运行`pip install -r requirements.txt`安装依赖

### Q: 为什么某些图表不显示？
A: 请检查浏览器控制台是否有错误信息，或尝试刷新页面

### Q: 如何更新模型？
A: 运行`python model_training/train_model.py`重新训练模型

### Q: 如何添加新的城市数据？
A: 将新数据放入数据目录，然后修改数据预处理脚本以支持新数据格式

## 📄 许可证

本项目仅供学习和研究使用。

## 🤝 贡献

欢迎对项目提出改进建议和Bug修复！

---

**运行方式**：`python main.py`
**项目主页**：PM2.5日级预测可视化大屏
**版本**：1.0.0
