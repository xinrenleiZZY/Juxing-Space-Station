# 京津冀PM2.5数据集特征说明文档

## 概述
本数据集包含从 2015-01-01 到 2026-01-19 的京津冀地区PM2.5浓度数据。
共包含 52481 条记录，32 个特征。

## 特征分类说明

### 1. 基础特征
| 字段名 | 数据类型 | 说明 |
|--------|----------|------|
| date | datetime64[ns] | 基础数据字段 |
| city | object | 基础数据字段 |
| pm25 | float64 | 基础数据字段 |
| data_quality_flag | int64 | 基础数据字段 |

### 2. 时间特征
| 字段名 | 数据类型 | 说明 |
|--------|----------|------|
| year | int32 | 时间维度特征 |
| month | int32 | 时间维度特征 |
| day | int32 | 时间维度特征 |
| season | int64 | 时间维度特征 |
| dayofweek | int32 | 时间维度特征 |
| is_weekend | int32 | 时间维度特征 |
| rolling_avg_7d | float64 | 7日滑动平均浓度 |
| rolling_avg_30d | float64 | 30日滑动平均浓度 |
| trend_30d | float64 | 最近30天趋势斜率 |
| year_over_year_change | float64 | 同比变化百分比 |

### 3. 污染事件特征
| 字段名 | 数据类型 | 说明 |
|--------|----------|------|
| pollution_event_id | object | 污染事件唯一标识符 |
| event_duration | int64 | 污染事件持续天数 |
| peak_intensity | float64 | 污染事件期间峰值浓度 |
| event_severity_index | float64 | 事件严重性综合指数 |

特征说明文档已保存至: c:\Users\xinre\Desktop\15\Juxing-Space-Station\数控中心\区级\京津冀PM2.5数据集数据特征工程\京津冀PM2.5数据特征工程\data\features\feature_documentation.md