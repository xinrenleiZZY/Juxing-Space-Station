# LSTM时间序列模型分析目录结构

## 总览

本目录结构基于LSTM时间序列模型分析的一般步骤设计，用于完成京津冀城市群PM2.5浓度的预测与可视化分析任务。

```
lstm_analysis/
├── configs/                # 配置文件目录
├── data_preparation/       # 数据准备目录
├── data_processing/        # 数据预处理目录
├── model_building/         # 模型构建目录
├── model_training/         # 模型训练目录
├── model_evaluation/       # 模型评估目录
├── visualization/          # 可视化分析目录
├── results/                # 结果保存目录
└── utils/                  # 工具函数目录
```

## 目录详情

### 1. configs/
**功能**：存储项目配置文件，统一管理参数设置。

**包含内容**：
- `model_config.py`：模型参数配置（LSTM层数、隐藏单元数、学习率等）
- `data_config.py`：数据处理参数配置（时间窗口大小、特征选择等）
- `train_config.py`：训练参数配置（批大小、迭代次数、验证集比例等）
- `visual_config.py`：可视化参数配置（图表样式、颜色方案等）
- `city_config.py`：京津冀城市列表配置

**用途**：便于参数调整和实验复现，集中管理所有配置信息。

### 2. data_preparation/
**功能**：原始数据的收集、整合和初步整理。

**包含内容**：
- `data_loading.py`：从原始CSV文件加载数据
- `data_integration.py`：整合京津冀各城市数据
- `data_encoding.py`：数据编码（如城市名称编码）
- `data_exploration.py`：数据探索性分析脚本
- `raw_combined_data.csv`：整合后的原始数据集

**用途**：将分散的原始数据整合为统一的数据集，为后续处理做准备。

### 3. data_processing/
**功能**：数据预处理，包括清洗、归一化、特征工程等。

**包含内容**：
- `data_cleaning.py`：数据清洗（处理缺失值、异常值等）
- `data_normalization.py`：数据归一化/标准化
- `feature_engineering.py`：特征工程（生成时间特征、滞后特征等）
- `data_splitting.py`：数据集划分（训练集、验证集、测试集）
- `data_windowing.py`：时间序列窗口构建
- `processed_data.csv`：预处理后的数据集
- `windowed_data.npz`：构建好窗口的时间序列数据（numpy格式）

**用途**：将原始数据转化为适合LSTM模型训练的格式，提高模型性能。

### 4. model_building/
**功能**：LSTM模型的构建和定义。

**包含内容**：
- `lstm_model.py`：LSTM模型类定义
- `model_architecture.py`：模型架构设计
- `model_factory.py`：模型工厂（支持不同模型变体）
- `loss_functions.py`：自定义损失函数
- `metrics.py`：评估指标定义

**用途**：设计和实现LSTM时间序列预测模型，支持模型架构的灵活调整。

### 5. model_training/
**功能**：模型的训练和优化。

**包含内容**：
- `train_model.py`：模型训练主脚本
- `hyperparameter_tuning.py`：超参数调优
- `early_stopping.py`：早停机制实现
- `model_checkpoint.py`：模型保存与加载
- `training_logs/`：训练日志目录
- `saved_models/`：训练好的模型目录

**用途**：训练LSTM模型，优化模型参数，保存训练过程和结果。

### 6. model_evaluation/
**功能**：模型的评估和性能分析。

**包含内容**：
- `evaluate_model.py`：模型评估主脚本
- `performance_metrics.py`：计算评估指标
- `error_analysis.py`：误差分析
- `model_comparison.py`：不同模型或参数的比较
- `evaluation_results.csv`：评估结果汇总

**用途**：评估模型性能，分析预测误差，比较不同模型变体。

### 7. visualization/
**功能**：数据可视化和结果展示。

**包含内容**：
- `data_visualization.py`：数据可视化（原始数据趋势、特征分布等）
- `model_visualization.py`：模型结果可视化（预测值与真实值对比等）
- `error_visualization.py`：误差可视化（残差图、误差分布等）
- `spatial_visualization.py`：空间可视化（京津冀地区PM2.5浓度空间分布）
- `plots/`：生成的图表目录
- `interactive_dashboard.py`：交互式可视化仪表盘

**用途**：直观展示数据特征、模型性能和预测结果，辅助分析和决策。

### 8. results/
**功能**：分析结果的汇总和保存。

**包含内容**：
- `predictions.csv`：模型预测结果
- `final_report.md`：最终分析报告
- `model_performance_summary.md`：模型性能总结
- `parameter_experiments/`：参数实验结果目录
- `case_studies/`：案例分析目录

**用途**：保存和管理分析结果，便于后续查阅和分享。

### 9. utils/
**功能**：通用工具函数和辅助模块。

**包含内容**：
- `file_utils.py`：文件读写工具
- `date_utils.py`：日期时间处理工具
- `math_utils.py`：数学计算工具
- `logging_utils.py`：日志记录工具
- `plotting_utils.py`：绘图辅助工具

**用途**：提供通用功能支持，减少代码重复，提高代码复用性。

## 使用流程

1. **数据准备**：在`data_preparation`目录下加载和整合原始数据
2. **数据预处理**：在`data_processing`目录下对数据进行清洗和特征工程
3. **模型构建**：在`model_building`目录下设计和实现LSTM模型
4. **模型训练**：在`model_training`目录下训练和优化模型
5. **模型评估**：在`model_evaluation`目录下评估模型性能
6. **可视化分析**：在`visualization`目录下生成可视化图表
7. **结果保存**：将最终结果保存到`results`目录

## 扩展建议

- 根据实际需求调整目录结构
- 增加版本控制（如使用git）
- 添加文档说明，便于团队协作
- 考虑使用Docker进行环境封装

---

**创建时间**：2026年1月17日
**用途**：京津冀城市群PM2.5浓度的预测与可视化分析