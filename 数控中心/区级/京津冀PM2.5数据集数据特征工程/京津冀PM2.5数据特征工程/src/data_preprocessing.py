# src/data_preprocessing.py
import pandas as pd
import numpy as np
from pathlib import Path
import warnings
import sys
warnings.filterwarnings('ignore')

# 添加项目根目录到Python路径，以便在直接运行时也能导入config模块
sys.path.append(str(Path(__file__).parent.parent))

from config.settings import *

class DataPreprocessor:
    def __init__(self, raw_data_path=None):
        """
        初始化数据预处理器
        
        Args:
            raw_data_path: 原始数据路径，如果为None则使用默认路径
        """
        if raw_data_path is None:
            self.raw_data_path = Path(RAW_DATA_DIR) / 'pm25_raw_data.csv'
        else:
            self.raw_data_path = Path(raw_data_path)
        
        self.processed_data_path = Path(PROCESSED_DATA_DIR) / 'pm25_processed.csv'
        
    def load_raw_data(self):
        """
        加载原始数据
        
        Returns:
            pd.DataFrame: 原始数据
        """
        print(f"正在加载原始数据: {self.raw_data_path}")
        try:
            # 假设原始数据格式为CSV，包含列：date, city, pm25
            df = pd.read_csv(self.raw_data_path)
            
            # 确保日期列为datetime类型
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
            
            print(f"数据加载成功，共 {len(df)} 条记录")
            print(f"时间范围: {df['date'].min()} 到 {df['date'].max()}")
            print(f"城市数量: {df['city'].nunique()}")
            print(f"原始城市列表: {sorted(df['city'].unique())}")
            
            return df
            
        except FileNotFoundError:
            print(f"错误: 找不到文件 {self.raw_data_path}")
            return None
    
    def standardize_city_names(self, df):
        """
        标准化城市名称，确保所有城市名称都带有"市"字
        
        Args:
            df: 原始数据框
            
        Returns:
            pd.DataFrame: 城市名称标准化后的数据框
        """
        print("\n=== 城市名称标准化 ===")
        
        # 创建城市名称映射字典
        city_mapping = {}
        for city in JINGJINJI_CITIES:
            # 提取不带"市"的城市名称作为键
            if city.endswith('市'):
                city_mapping[city[:-1]] = city
        
        # 标准化城市名称
        def standardize_city(city):
            if city in JINGJINJI_CITIES:
                return city
            elif city in city_mapping:
                return city_mapping[city]
            else:
                # 如果城市名称不在映射中，尝试添加"市"字
                standardized = city + '市'
                if standardized in JINGJINJI_CITIES:
                    return standardized
                return city
        
        # 应用标准化
        df_standardized = df.copy()
        df_standardized['city'] = df_standardized['city'].apply(standardize_city)
        
        # 检查标准化后的城市列表
        standardized_cities = sorted(df_standardized['city'].unique())
        print(f"标准化后城市列表: {standardized_cities}")
        
        # 检查是否有无法标准化的城市
        unknown_cities = [city for city in standardized_cities if city not in JINGJINJI_CITIES]
        if unknown_cities:
            print(f"警告: 以下城市不在京津冀城市列表中: {unknown_cities}")
        
        return df_standardized
    
    def data_quality_check(self, df):
        """
        数据质量检查和基本清洗（优化版本 - 使用配置参数）
        
        Args:
            df: 原始数据框
            
        Returns:
            pd.DataFrame: 清洗后的数据
        """
        print("\n=== 数据质量检查 ===")
        original_count = len(df)
        
        config = DATA_PREPROCESSING_CONFIG
        
        # 1. 检查缺失值
        missing_before = df.isnull().sum().sum()
        print(f"缺失值数量: {missing_before}")
        
        # 2. 检查异常值（根据配置选择检测方法）
        if config['enable_outlier_detection']:
            outliers = self._detect_outliers(df, config)
            print(f"异常值数量: {len(outliers)}")
        else:
            outliers = pd.DataFrame()
            print("异常值检测已禁用")
        
        # 3. 过滤异常值（设为NaN，后续插补）
        df_clean = df.copy()
        if not outliers.empty:
            df_clean.loc[outliers.index, 'pm25'] = np.nan
        
        # 4. 处理重复记录
        if config['enable_duplicate_handling']:
            duplicate_count = df_clean.duplicated(subset=['date', 'city']).sum()
            print(f"重复的(date, city)记录数: {duplicate_count}")
            
            if duplicate_count > 0:
                print("处理重复记录，按日期和城市分组计算平均值...")
                df_clean = df_clean.groupby(['date', 'city'], as_index=False)['pm25'].mean()
        else:
            print("重复值处理已禁用")
        
        # 5. 数据完整性检查
        if config['enable_data_completeness_check']:
            date_range = pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='D')
            all_cities = JINGJINJI_CITIES
            full_index = pd.MultiIndex.from_product([date_range, all_cities], names=['date', 'city'])
            
            df_complete = df_clean.set_index(['date', 'city']).reindex(full_index).reset_index()
        else:
            df_complete = df_clean
            print("数据完整性检查已禁用")
        
        # 6. 标记数据质量
        df_complete['data_quality_flag'] = 0  # 0表示原始数据
        df_complete.loc[df_complete['pm25'].isna(), 'data_quality_flag'] = 1  # 1表示需要插补
        
        print(f"原始记录数: {original_count}")
        print(f"去重后记录数: {len(df_clean)}")
        print(f"完整化后记录数: {len(df_complete)}")
        print(f"需要插补的记录数: {df_complete['data_quality_flag'].sum()}")
        
        return df_complete
    
    def _detect_outliers(self, df, config):
        """
        检测异常值（支持多种方法）
        
        Args:
            df: 数据框
            config: 配置参数
            
        Returns:
            pd.DataFrame: 异常值索引
        """
        method = config['outlier_detection_method']
        
        if method == 'range':
            # 范围检测法
            valid_range = config['pm25_valid_range']
            return df[(df['pm25'] < valid_range[0]) | (df['pm25'] > valid_range[1])]
        
        elif method == 'iqr':
            # IQR方法
            Q1 = df['pm25'].quantile(0.25)
            Q3 = df['pm25'].quantile(0.75)
            IQR = Q3 - Q1
            multiplier = config['iqr_multiplier']
            lower_bound = Q1 - multiplier * IQR
            upper_bound = Q3 + multiplier * IQR
            return df[(df['pm25'] < lower_bound) | (df['pm25'] > upper_bound)]
        
        elif method == 'zscore':
            # Z-score方法
            mean = df['pm25'].mean()
            std = df['pm25'].std()
            threshold = config['zscore_threshold']
            z_scores = np.abs((df['pm25'] - mean) / std)
            return df[z_scores > threshold]
        
        else:
            print(f"警告: 未知的异常值检测方法 '{method}'，使用默认范围检测")
            valid_range = config['pm25_valid_range']
            return df[(df['pm25'] < valid_range[0]) | (df['pm25'] > valid_range[1])]
    
    def interpolate_missing_data(self, df):
        """
        缺失数据插补（优化版本 - 使用向量化操作）
        
        Args:
            df: 包含缺失值的数据框
            
        Returns:
            pd.DataFrame: 插补后的数据
        """
        print("\n=== 缺失数据插补 ===")
        
        # 使用向量化操作替代循环，提高性能
        df_interpolated = df.copy()
        
        # 记录插补前的缺失状态
        missing_before = df_interpolated['pm25'].isna()
        
        # 按城市分组进行插补（向量化操作）
        def interpolate_group(group):
            group['pm25'] = group['pm25'].interpolate(method='linear', limit_direction='both')
            return group
        
        df_interpolated = df_interpolated.groupby('city', group_keys=False).apply(interpolate_group)
        
        # 更新数据质量标志
        missing_after = df_interpolated['pm25'].isna()
        newly_filled = missing_before & ~missing_after
        df_interpolated.loc[newly_filled, 'data_quality_flag'] = 2  # 2表示插补数据
        
        # 检查是否还有缺失值
        remaining_missing = df_interpolated['pm25'].isna().sum()
        print(f"插补后剩余缺失值: {remaining_missing}")
        
        # 如果还有缺失值，使用区域平均值填充
        if remaining_missing > 0:
            print("使用区域日平均值填充剩余缺失值...")
            
            # 计算每日区域平均值
            daily_avg = df_interpolated.groupby('date')['pm25'].transform('mean')
            
            # 用区域平均值填充剩余缺失值
            missing_mask = df_interpolated['pm25'].isna()
            df_interpolated.loc[missing_mask, 'pm25'] = daily_avg[missing_mask]
            df_interpolated.loc[missing_mask, 'data_quality_flag'] = 3  # 3表示使用区域平均值填充
        
        print("数据插补完成")
        return df_interpolated
    
    def run_pipeline(self, save_output=True):
        """
        运行完整的数据预处理流程
        
        Args:
            save_output: 是否保存处理结果
            
        Returns:
            pd.DataFrame: 处理后的数据
        """
        print("开始数据预处理流程...")
        
        # 1. 加载原始数据
        df_raw = self.load_raw_data()
        if df_raw is None:
            return None
        
        # 2. 城市名称标准化
        df_standardized = self.standardize_city_names(df_raw)
        
        # 3. 数据质量检查
        df_clean = self.data_quality_check(df_standardized)
        
        # 4. 缺失数据插补
        df_final = self.interpolate_missing_data(df_clean)
        
        # 5. 数据统计分析
        self._analyze_data(df_final)
        
        # 6. 保存处理结果
        if save_output:
            # 确保输出目录存在
            Path(PROCESSED_DATA_DIR).mkdir(parents=True, exist_ok=True)
            
            df_final.to_csv(self.processed_data_path, index=False)
            print(f"\n处理后的数据已保存至: {self.processed_data_path}")
        
        return df_final
    
    def _analyze_data(self, df):
        """
        数据统计分析
        
        Args:
            df: 处理后的数据框
        """
        print("\n=== 数据统计分析 ===")
        
        # 基本统计
        print(f"时间范围: {df['date'].min().date()} 到 {df['date'].max().date()}")
        print(f"总天数: {df['date'].nunique()}")
        print(f"数据点总数: {len(df)}")
        
        # 数据质量统计
        quality_counts = df['data_quality_flag'].value_counts().sort_index()
        quality_labels = {
            0: '原始数据',
            1: '标记为缺失(已插补)',
            2: '时间序列插补',
            3: '区域平均值填充'
        }
        
        print("\n数据质量分布:")
        for flag, count in quality_counts.items():
            label = quality_labels.get(flag, f'未知({flag})')
            print(f"  {label}: {count}条 ({count/len(df)*100:.2f}%)")
        
        # 各城市数据完整性
        print("\n各城市数据完整性:")
        for city in JINGJINJI_CITIES:
            city_data = df[df['city'] == city]
            missing_rate = (city_data['data_quality_flag'] > 0).mean() * 100
            print(f"  {city}: 缺失/插补率 {missing_rate:.1f}%")
        
        # PM2.5浓度统计
        print(f"\nPM2.5浓度统计:")
        print(f"  平均值: {df['pm25'].mean():.2f} μg/m³")
        print(f"  中位数: {df['pm25'].median():.2f} μg/m³")
        print(f"  标准差: {df['pm25'].std():.2f} μg/m³")
        print(f"  最小值: {df['pm25'].min():.2f} μg/m³")
        print(f"  最大值: {df['pm25'].max():.2f} μg/m³")

if __name__ == "__main__":
    """
    测试数据预处理流程
    """
    print("=" * 60)
    print("测试数据预处理流程")
    print("=" * 60)
    
    # 初始化预处理器
    preprocessor = DataPreprocessor()
    
    # 运行预处理流程
    result = preprocessor.run_pipeline(save_output=True)
    
    if result is not None:
        print("\n测试完成: 数据预处理流程执行成功!")
    else:
        print("\n测试完成: 数据预处理流程执行失败!")