# config/settings.py
import os
from datetime import datetime

# 路径配置
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
FEATURES_DIR = os.path.join(DATA_DIR, 'features')
EXTERNAL_DATA_DIR = os.path.join(DATA_DIR, 'external')

# 京津冀城市列表
JINGJINJI_CITIES = [
    '北京市', '天津市', '石家庄市', '唐山市', '秦皇岛市', '邯郸市', 
    '邢台市', '保定市', '张家口市', '承德市', '沧州市', '廊坊市', '衡水市'
]

# 城市坐标映射（用于空间分析）
CITY_COORDINATES = {
    '北京市': {'lon': 116.4074, 'lat': 39.9042},
    '天津市': {'lon': 117.1902, 'lat': 39.1256},
    '石家庄市': {'lon': 114.4995, 'lat': 38.1006},
    # ... 添加其他城市坐标
}

# 政策时间线（用于政策分析）
POLICY_PERIODS = {
    '大气十条时期': ('2013-09-01', '2017-12-31'),
    '蓝天保卫战时期': ('2018-01-01', '2020-12-31'),
    '十四五深化治理时期': ('2021-01-01', '2025-12-31'),
}

# 重大活动时间线
SPECIAL_EVENTS = {
    'APEC会议': ('2014-11-05', '2014-11-11'),
    '抗战胜利阅兵': ('2015-09-01', '2015-09-03'),
    'G20峰会': ('2016-09-01', '2016-09-05'),
    '一带一路峰会': ('2017-05-14', '2017-05-15'),
    '冬奥会': ('2022-02-04', '2022-02-20'),
}

# 污染阈值定义
POLLUTION_THRESHOLDS = {
    'pm25_grade_1': 35,    # 国家一级标准（优）
    'pm25_grade_2': 75,    # 国家二级标准（良/轻度污染界限）
    'pm25_grade_3': 115,   # 中度污染
    'pm25_grade_4': 150,   # 重度污染
    'pm25_grade_5': 250,   # 严重污染
}

# 数据预处理配置
DATA_PREPROCESSING_CONFIG = {
    'pm25_valid_range': (0, 1000),  # PM2.5浓度合理范围
    'interpolation_method': 'linear',  # 插值方法
    'interpolation_limit_direction': 'both',  # 插值方向
    'enable_duplicate_handling': True,  # 是否启用重复值处理
    'enable_outlier_detection': True,  # 是否启用异常值检测
    'enable_data_completeness_check': True,  # 是否启用数据完整性检查
    'max_missing_rate': 0.5,  # 最大缺失率阈值
    'outlier_detection_method': 'range',  # 异常值检测方法: 'range', 'iqr', 'zscore'
    'iqr_multiplier': 1.5,  # IQR方法倍数
    'zscore_threshold': 3,  # Z-score阈值
}