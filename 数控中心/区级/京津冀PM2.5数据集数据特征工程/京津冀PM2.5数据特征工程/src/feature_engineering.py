# src/feature_engineering.py
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import warnings
import sys
warnings.filterwarnings('ignore')

# 添加项目根目录到Python路径，以便在直接运行时也能导入config模块
sys.path.append(str(Path(__file__).parent.parent))

from config.settings import *

class FeatureEngineer:
    def __init__(self, processed_data_path=None):
        """
        初始化特征工程师
        
        Args:
            processed_data_path: 处理后的数据路径
        """
        if processed_data_path is None:
            self.processed_data_path = Path(PROCESSED_DATA_DIR) / 'pm25_processed.csv'
        else:
            self.processed_data_path = Path(processed_data_path)
        
        self.features_data_path = Path(FEATURES_DIR) / 'pm25_with_features.csv'
        
    def load_processed_data(self):
        """
        加载处理后的数据
        
        Returns:
            pd.DataFrame: 处理后的数据
        """
        print(f"正在加载处理后的数据: {self.processed_data_path}")
        
        try:
            df = pd.read_csv(self.processed_data_path)
            
            # 确保日期列为datetime类型
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
            
            print(f"数据加载成功，共 {len(df)} 条记录")
            return df
            
        except FileNotFoundError:
            print(f"错误: 找不到文件 {self.processed_data_path}")
            return None
    
    def create_time_features(self, df):
        """
        创建时间相关特征
        
        Args:
            df: 处理后的数据框
            
        Returns:
            pd.DataFrame: 添加了时间特征的数据框
        """
        print("\n=== 创建时间特征 ===")
        df_featured = df.copy()
        
        # 1. 基础时间特征
        df_featured['year'] = df_featured['date'].dt.year
        df_featured['month'] = df_featured['date'].dt.month
        df_featured['day'] = df_featured['date'].dt.day
        df_featured['dayofweek'] = df_featured['date'].dt.dayofweek  # 周一=0, 周日=6
        df_featured['quarter'] = df_featured['date'].dt.quarter
        df_featured['is_weekend'] = df_featured['dayofweek'].isin([5, 6]).astype(int)
        
        # 2. 季节特征
        df_featured['season'] = df_featured['month'].apply(
            lambda m: 1 if m in [3,4,5] else  # 春季
                      2 if m in [6,7,8] else  # 夏季
                      3 if m in [9,10,11] else  # 秋季
                      4  # 冬季
        )
        
        # 3. 滑动平均和趋势特征（按城市计算）
        print("  计算滑动平均和趋势特征...")
        
        for city in JINGJINJI_CITIES:
            city_mask = df_featured['city'] == city
            
            # 按日期排序
            city_data = df_featured[city_mask].sort_values('date')
            
            # 7日滑动平均
            df_featured.loc[city_mask, 'rolling_avg_7d'] = city_data['pm25'].rolling(7, min_periods=3).mean().values
            
            # 30日滑动平均
            df_featured.loc[city_mask, 'rolling_avg_30d'] = city_data['pm25'].rolling(30, min_periods=15).mean().values
            
            # 30日趋势（线性回归斜率）
            def calculate_trend(series):
                if len(series) < 30:
                    return np.nan
                x = np.arange(len(series))
                y = series.values
                coef = np.polyfit(x, y, 1)
                return coef[0]  # 斜率
            
            df_featured.loc[city_mask, 'trend_30d'] = (
                city_data['pm25'].rolling(30, min_periods=15).apply(calculate_trend, raw=False).values
            )
        
        # 4. 年际变化特征
        print("  计算年际变化特征...")
        df_featured['year_over_year_change'] = np.nan
        
        for city in JINGJINJI_CITIES:
            city_mask = df_featured['city'] == city
            city_data = df_featured[city_mask].sort_values('date')
            
            # 计算日期的年-月-日组合
            city_data['month_day'] = city_data['month'].astype(str) + '-' + city_data['day'].astype(str)
            
            # 计算同比变化（与去年同一天的差异）
            for idx in range(1, len(city_data)):
                current_date = city_data.iloc[idx]['date']
                last_year_date = current_date - pd.DateOffset(years=1)
                
                # 查找去年同一天的数据
                last_year_mask = (city_data['date'] == last_year_date)
                if last_year_mask.any():
                    current_val = city_data.iloc[idx]['pm25']
                    last_year_val = city_data[last_year_mask]['pm25'].values[0]
                    
                    if not pd.isna(current_val) and not pd.isna(last_year_val):
                        yoy_change = ((current_val - last_year_val) / last_year_val) * 100
                        df_featured.loc[city_data.index[idx], 'year_over_year_change'] = yoy_change
        
        print("  时间特征创建完成")
        return df_featured
    
    def create_pollution_event_features(self, df):
        """
        创建污染事件相关特征
        
        Args:
            df: 数据框
            
        Returns:
            pd.DataFrame: 添加了污染事件特征的数据框
        """
        print("\n=== 创建污染事件特征 ===")
        
        df_event = df.copy()
        
        # 污染事件识别参数
        EVENT_THRESHOLD = 75  # 污染阈值 (μg/m³)
        MIN_EVENT_DURATION = 3  # 最小污染事件持续时间（天）
        MAX_BREAK_DURATION = 2  # 最大允许中断天数（浓度低于50）
        
        # 初始化污染事件ID
        df_event['pollution_event_id'] = np.nan
        df_event['event_duration'] = 0
        df_event['peak_intensity'] = 0
        df_event['event_severity_index'] = 0
        
        event_counter = 0
        
        for city in JINGJINJI_CITIES:
            print(f"  处理城市: {city}")
            city_mask = df_event['city'] == city
            city_data = df_event[city_mask].sort_values('date').reset_index(drop=True)
            
            # 保存原始索引以便更新
            original_indices = df_event[city_mask].sort_values('date').index.tolist()
            
            # 标记污染日
            city_data['is_polluted'] = (city_data['pm25'] > EVENT_THRESHOLD).astype(int)
            
            # 识别污染事件
            in_event = False
            event_start_idx = 0
            event_days = 0
            event_max_pm25 = 0
            
            for i in range(len(city_data)):
                current_polluted = city_data.loc[i, 'is_polluted'] == 1
                
                if not in_event and current_polluted:
                    # 开始新事件
                    in_event = True
                    event_start_idx = i
                    event_days = 1
                    event_max_pm25 = city_data.loc[i, 'pm25']
                    
                elif in_event and current_polluted:
                    # 事件持续
                    event_days += 1
                    event_max_pm25 = max(event_max_pm25, city_data.loc[i, 'pm25'])
                    
                elif in_event and not current_polluted:
                    # 检查是否应该结束事件
                    # 查找后续几天的数据
                    lookahead_limit = min(MAX_BREAK_DURATION, len(city_data) - i - 1)
                    will_continue = False
                    
                    for j in range(1, lookahead_limit + 1):
                        if city_data.loc[i + j, 'is_polluted'] == 1:
                            will_continue = True
                            break
                    
                    if not will_continue:
                        # 结束事件
                        if event_days >= MIN_EVENT_DURATION:
                            event_counter += 1
                            event_id = f"E{city[:2]}{event_counter:04d}"
                            
                            # 计算事件严重性指数
                            avg_pm25 = city_data.loc[event_start_idx:i, 'pm25'].mean()
                            severity_index = avg_pm25 * np.log(event_days + 1)
                            
                            # 更新数据 - 使用原始索引
                            for idx in range(event_start_idx, i):
                                original_idx = original_indices[idx]
                                df_event.loc[original_idx, 'pollution_event_id'] = event_id
                                df_event.loc[original_idx, 'event_duration'] = event_days
                                df_event.loc[original_idx, 'peak_intensity'] = event_max_pm25
                                df_event.loc[original_idx, 'event_severity_index'] = severity_index
                        
                        # 重置事件状态
                        in_event = False
                        event_days = 0
                        event_max_pm25 = 0
        
        print(f"  共识别出 {event_counter} 个污染事件")
        return df_event
    
    def create_spatial_features(self, df):
        """
        创建空间相关特征
        
        Args:
            df: 数据框
            
        Returns:
            pd.DataFrame: 添加了空间特征的数据框
        """
        print("\n=== 创建空间特征 ===")
        
        df_spatial = df.copy()
        
        # 1. 计算每日区域统计数据
        print("  计算区域统计数据...")
        
        # 按日期计算区域平均值
        daily_region_avg = df_spatial.groupby('date')['pm25'].mean().reset_index()
        daily_region_avg.rename(columns={'pm25': 'regional_avg_pm25'}, inplace=True)
        
        # 合并到原始数据
        df_spatial = pd.merge(df_spatial, daily_region_avg, on='date', how='left')
        
        # 2. 计算偏离区域均值程度
        df_spatial['deviation_from_regional_avg'] = (
            (df_spatial['pm25'] - df_spatial['regional_avg_pm25']) / df_spatial['regional_avg_pm25'] * 100
        )
        
        # 3. 计算区域排名
        print("  计算每日区域排名...")
        
        # 每日计算各城市排名
        df_spatial['regional_rank'] = df_spatial.groupby('date')['pm25'].rank(
            method='min', ascending=False
        )
        
        # 4. 识别区域热点（优化版本）
        df_spatial['is_regional_hotspot'] = 0
        
        # 热点条件：连续3天排名前5且浓度高于区域平均30%
        for city in JINGJINJI_CITIES:
            city_mask = df_spatial['city'] == city
            city_data = df_spatial[city_mask].sort_values('date').reset_index(drop=True)
            
            # 保存原始索引
            original_indices = df_spatial[city_mask].sort_values('date').index.tolist()
            
            for i in range(2, len(city_data)):
                # 检查连续3天
                rank_condition = all(city_data.loc[i-j, 'regional_rank'] <= 5 for j in range(3))
                deviation_condition = all(city_data.loc[i-j, 'deviation_from_regional_avg'] > 30 for j in range(3))
                
                if rank_condition and deviation_condition:
                    # 使用原始索引更新
                    for j in range(3):
                        original_idx = original_indices[i-j]
                        df_spatial.loc[original_idx, 'is_regional_hotspot'] = 1
        
        print("  空间特征创建完成")
        return df_spatial
    
    def create_policy_features(self, df):
        """
        创建政策相关特征
        
        Args:
            df: 数据框
            
        Returns:
            pd.DataFrame: 添加了政策特征的数据框
        """
        print("\n=== 创建政策特征 ===")
        
        df_policy = df.copy()
        
        # 1. 政策时期标签
        df_policy['policy_period'] = '其他时期'
        
        for period_name, (start_date, end_date) in POLICY_PERIODS.items():
            mask = (df_policy['date'] >= pd.to_datetime(start_date)) & \
                   (df_policy['date'] <= pd.to_datetime(end_date))
            df_policy.loc[mask, 'policy_period'] = period_name
        
        # 2. 重大活动标志
        df_policy['special_event_flag'] = 0
        
        for event_name, (start_date, end_date) in SPECIAL_EVENTS.items():
            mask = (df_policy['date'] >= pd.to_datetime(start_date)) & \
                   (df_policy['date'] <= pd.to_datetime(end_date))
            df_policy.loc[mask, 'special_event_flag'] = 1
        
        # 3. 计算政策实施前后变化
        print("  计算政策效果指标...")
        
        # 对每个政策时期，计算实施前后对比
        policy_effects = []
        
        for period_name, (start_date, end_date) in POLICY_PERIODS.items():
            start_dt = pd.to_datetime(start_date)
            end_dt = pd.to_datetime(end_date)
            
            # 政策实施前一年
            before_start = start_dt - pd.DateOffset(years=1)
            
            # 政策实施期间
            during_policy = df_policy[
                (df_policy['date'] >= start_dt) & 
                (df_policy['date'] <= end_dt)
            ]
            
            # 政策实施前同期
            before_policy = df_policy[
                (df_policy['date'] >= before_start) & 
                (df_policy['date'] < start_dt)
            ]
            
            if not during_policy.empty and not before_policy.empty:
                # 计算平均浓度变化
                avg_during = during_policy['pm25'].mean()
                avg_before = before_policy['pm25'].mean()
                change_pct = ((avg_during - avg_before) / avg_before) * 100
                
                policy_effects.append({
                    'policy_period': period_name,
                    'avg_before': avg_before,
                    'avg_during': avg_during,
                    'change_pct': change_pct
                })
        
        # 保存政策效果分析
        policy_effects_df = pd.DataFrame(policy_effects)
        policy_effects_path = Path(FEATURES_DIR) / 'policy_effects_analysis.csv'
        policy_effects_df.to_csv(policy_effects_path, index=False)
        print(f"  政策效果分析已保存至: {policy_effects_path}")
        
        print("  政策特征创建完成")
        return df_policy
    
    def create_health_risk_features(self, df):
        """
        创建健康风险相关特征
        
        Args:
            df: 数据框
            
        Returns:
            pd.DataFrame: 添加了健康风险特征的数据框
        """
        print("\n=== 创建健康风险特征 ===")
        
        df_health = df.copy()
        
        # 1. AQI等级分类
        def pm25_to_aqi(pm25):
            """根据PM2.5浓度计算AQI等级"""
            if pd.isna(pm25):
                return '未知'
            elif pm25 <= 35:
                return '优'
            elif pm25 <= 75:
                return '良'
            elif pm25 <= 115:
                return '轻度污染'
            elif pm25 <= 150:
                return '中度污染'
            elif pm25 <= 250:
                return '重度污染'
            else:
                return '严重污染'
        
        df_health['aqi_category'] = df_health['pm25'].apply(pm25_to_aqi)
        
        # 2. 超标标志
        df_health['exceedance_flag_35'] = (df_health['pm25'] > 35).astype(int)
        df_health['exceedance_flag_75'] = (df_health['pm25'] > 75).astype(int)
        
        # 3. 累计暴露量（按城市计算 - 优化版本）
        print("  计算累计暴露量...")
        
        df_health['cumulative_exposure_7d'] = 0
        df_health['cumulative_exposure_30d'] = 0
        df_health['cumulative_exposure_365d'] = 0
        
        for city in JINGJINJI_CITIES:
            city_mask = df_health['city'] == city
            city_data = df_health[city_mask].sort_values('date').reset_index(drop=True)
            
            # 保存原始索引
            original_indices = df_health[city_mask].sort_values('date').index.tolist()
            
            # 使用向量化操作计算滚动累计
            exceedance_series = city_data['exceedance_flag_35']
            
            # 7天滑动窗口
            rolling_7d = exceedance_series.rolling(7, min_periods=1).sum()
            
            # 30天滑动窗口
            rolling_30d = exceedance_series.rolling(30, min_periods=1).sum()
            
            # 365天滑动窗口
            rolling_365d = exceedance_series.rolling(365, min_periods=1).sum()
            
            # 更新原始数据框
            for i in range(len(city_data)):
                original_idx = original_indices[i]
                df_health.loc[original_idx, 'cumulative_exposure_7d'] = rolling_7d.iloc[i]
                df_health.loc[original_idx, 'cumulative_exposure_30d'] = rolling_30d.iloc[i]
                df_health.loc[original_idx, 'cumulative_exposure_365d'] = rolling_365d.iloc[i]
        
        # 4. 超标负担（超标浓度的累计和 - 优化版本）
        print("  计算超标负担...")
        
        df_health['exceedance_burden_365d'] = 0
        
        for city in JINGJINJI_CITIES:
            city_mask = df_health['city'] == city
            city_data = df_health[city_mask].sort_values('date').reset_index(drop=True)
            
            # 保存原始索引
            original_indices = df_health[city_mask].sort_values('date').index.tolist()
            
            # 计算超标部分
            exceedance_values = (city_data['pm25'] - 35).clip(lower=0)
            
            # 使用向量化操作计算365天滑动窗口
            rolling_burden = exceedance_values.rolling(365, min_periods=1).sum()
            
            # 更新原始数据框
            for i in range(len(city_data)):
                original_idx = original_indices[i]
                df_health.loc[original_idx, 'exceedance_burden_365d'] = rolling_burden.iloc[i]
        
        print("  健康风险特征创建完成")
        return df_health
    
    def run_pipeline(self, save_output=True):
        """
        运行完整的特征工程流程
        
        Args:
            save_output: 是否保存结果
            
        Returns:
            pd.DataFrame: 包含所有特征的数据框
        """
        print("开始特征工程流程...")
        
        # 1. 加载处理后的数据
        df = self.load_processed_data()
        if df is None:
            return None
        
        # 2. 确保数据按城市和日期排序
        df = df.sort_values(['city', 'date']).reset_index(drop=True)
        
        # 3. 创建时间特征
        df = self.create_time_features(df)
        
        # 4. 创建污染事件特征
        df = self.create_pollution_event_features(df)
        
        # 5. 创建空间特征
        df = self.create_spatial_features(df)
        
        # 6. 创建政策特征
        df = self.create_policy_features(df)
        
        # 7. 创建健康风险特征
        df = self.create_health_risk_features(df)
        
        # 8. 特征统计分析
        self._analyze_features(df)
        
        # 9. 保存结果
        if save_output:
            # 确保输出目录存在
            Path(FEATURES_DIR).mkdir(parents=True, exist_ok=True)
            
            # 保存完整数据集
            df.to_csv(self.features_data_path, index=False)
            print(f"\n特征工程结果已保存至: {self.features_data_path}")
            
            # 保存字段说明文档
            self._save_feature_documentation(df)
        
        return df
    
    def _analyze_features(self, df):
        """
        特征统计分析
        
        Args:
            df: 包含所有特征的数据框
        """
        print("\n=== 特征统计分析 ===")
        
        # 统计各类特征数量
        time_features = [col for col in df.columns if col in ['year', 'month', 'day', 'season', 
                                                              'rolling_avg_7d', 'rolling_avg_30d', 
                                                              'trend_30d', 'year_over_year_change']]
        
        event_features = [col for col in df.columns if 'event' in col.lower()]
        
        spatial_features = [col for col in df.columns if 'regional' in col.lower() or 
                           'hotspot' in col.lower() or 'deviation' in col.lower()]
        
        policy_features = [col for col in df.columns if 'policy' in col.lower() or 
                          'special' in col.lower()]
        
        health_features = [col for col in df.columns if 'exceedance' in col.lower() or 
                          'exposure' in col.lower() or 'burden' in col.lower() or 
                          'aqi' in col.lower()]
        
        print(f"总特征数量: {len(df.columns)}")
        print(f"时间特征: {len(time_features)}个")
        print(f"污染事件特征: {len(event_features)}个")
        print(f"空间特征: {len(spatial_features)}个")
        print(f"政策特征: {len(policy_features)}个")
        print(f"健康风险特征: {len(health_features)}个")
        
        # 污染事件统计
        event_cities = df[~df['pollution_event_id'].isna()]['city'].nunique()
        event_count = df['pollution_event_id'].nunique()
        print(f"\n污染事件覆盖城市: {event_cities}个")
        print(f"识别污染事件总数: {event_count}个")
        
        # AQI等级分布
        print("\nAQI等级分布:")
        aqi_dist = df['aqi_category'].value_counts()
        for category, count in aqi_dist.items():
            percentage = count / len(df) * 100
            print(f"  {category}: {count}天 ({percentage:.1f}%)")
        
        # 政策时期数据分布
        print("\n政策时期数据分布:")
        policy_dist = df['policy_period'].value_counts()
        for period, count in policy_dist.items():
            years = count / (len(JINGJINJI_CITIES) * 365)  # 估算年数
            print(f"  {period}: {count}条记录 (约{years:.1f}年数据)")
    
    def _save_feature_documentation(self, df):
        """
        保存特征说明文档
        
        Args:
            df: 包含所有特征的数据框
        """
        doc_path = Path(FEATURES_DIR) / 'feature_documentation.md'
        
        with open(doc_path, 'w', encoding='utf-8') as f:
            f.write("# 京津冀PM2.5数据集特征说明文档\n\n")
            f.write("## 概述\n")
            f.write(f"本数据集包含从 {df['date'].min().date()} 到 {df['date'].max().date()} 的京津冀地区PM2.5浓度数据。\n")
            f.write(f"共包含 {len(df)} 条记录，{len(df.columns)} 个特征。\n\n")
            
            f.write("## 特征分类说明\n\n")
            
            # 基础特征
            f.write("### 1. 基础特征\n")
            f.write("| 字段名 | 数据类型 | 说明 |\n")
            f.write("|--------|----------|------|\n")
            base_features = ['date', 'city', 'pm25', 'data_quality_flag']
            for feat in base_features:
                if feat in df.columns:
                    f.write(f"| {feat} | {df[feat].dtype} | 基础数据字段 |\n")
            
            # 时间特征
            f.write("\n### 2. 时间特征\n")
            f.write("| 字段名 | 数据类型 | 说明 |\n")
            f.write("|--------|----------|------|\n")
            time_features = ['year', 'month', 'day', 'season', 'dayofweek', 'is_weekend', 
                            'rolling_avg_7d', 'rolling_avg_30d', 'trend_30d', 'year_over_year_change']
            for feat in time_features:
                if feat in df.columns:
                    desc = {
                        'rolling_avg_7d': '7日滑动平均浓度',
                        'rolling_avg_30d': '30日滑动平均浓度',
                        'trend_30d': '最近30天趋势斜率',
                        'year_over_year_change': '同比变化百分比'
                    }.get(feat, '时间维度特征')
                    f.write(f"| {feat} | {df[feat].dtype} | {desc} |\n")
            
            # 污染事件特征
            f.write("\n### 3. 污染事件特征\n")
            f.write("| 字段名 | 数据类型 | 说明 |\n")
            f.write("|--------|----------|------|\n")
            event_features = ['pollution_event_id', 'event_duration', 'peak_intensity', 'event_severity_index']
            for feat in event_features:
                if feat in df.columns:
                    desc = {
                        'pollution_event_id': '污染事件唯一标识符',
                        'event_duration': '污染事件持续天数',
                        'peak_intensity': '污染事件期间峰值浓度',
                        'event_severity_index': '事件严重性综合指数'
                    }.get(feat, '污染事件特征')
                    f.write(f"| {feat} | {df[feat].dtype} | {desc} |\n")
            
            f.write(f"\n特征说明文档已保存至: {doc_path}")

if __name__ == "__main__":
    """
    测试特征工程流程
    """
    print("=" * 60)
    print("测试特征工程流程")
    print("=" * 60)
    
    # 初始化特征工程师
    engineer = FeatureEngineer()
    
    # 运行特征工程流程
    result = engineer.run_pipeline(save_output=True)
    
    if result is not None:
        print("\n测试完成: 特征工程流程执行成功!")
    else:
        print("\n测试完成: 特征工程流程执行失败!")