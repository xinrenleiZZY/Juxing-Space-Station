# src/data_analysis.py
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import sys
warnings.filterwarnings('ignore')

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent))

from config.settings import *

class DataAnalyzer:
    def __init__(self, features_data_path=None):
        """
        初始化数据分析器
        
        Args:
            features_data_path: 特征数据路径
        """
        if features_data_path is None:
            self.features_data_path = Path(FEATURES_DIR) / 'pm25_with_features.csv'
        else:
            self.features_data_path = Path(features_data_path)
        
        self.output_dir = Path(FEATURES_DIR) / 'analysis_results'
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def load_features_data(self):
        """
        加载特征数据
        
        Returns:
            pd.DataFrame: 特征数据
        """
        print(f"正在加载特征数据: {self.features_data_path}")
        
        try:
            df = pd.read_csv(self.features_data_path)
            
            # 确保日期列为datetime类型
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
            
            print(f"数据加载成功，共 {len(df)} 条记录")
            return df
            
        except FileNotFoundError:
            print(f"错误: 找不到文件 {self.features_data_path}")
            return None
    
    def data_quality_validation(self, df):
        """
        数据质量验证
        
        Args:
            df: 特征数据框
            
        Returns:
            dict: 质量验证结果
        """
        print("\n=== 数据质量验证 ===")
        
        validation_results = {}
        
        # 1. 基础信息
        validation_results['basic_info'] = {
            'total_records': len(df),
            'total_features': len(df.columns),
            'time_range': (df['date'].min(), df['date'].max()),
            'cities': df['city'].unique().tolist(),
            'city_count': df['city'].nunique()
        }
        
        # 2. 缺失值检查
        missing_stats = df.isnull().sum()
        missing_stats = missing_stats[missing_stats > 0]
        validation_results['missing_values'] = {
            'total_missing': missing_stats.sum(),
            'missing_features': missing_stats.to_dict(),
            'missing_rate': (missing_stats.sum() / (len(df) * len(df.columns))) * 100
        }
        
        # 3. 数据范围检查
        validation_results['data_ranges'] = {
            'pm25_range': (df['pm25'].min(), df['pm25'].max()),
            'pm25_mean': df['pm25'].mean(),
            'pm25_std': df['pm25'].std()
        }
        
        # 4. 特征完整性检查
        expected_features = [
            'date', 'city', 'pm25', 'data_quality_flag',
            'year', 'month', 'season', 'rolling_avg_7d', 'rolling_avg_30d',
            'pollution_event_id', 'event_duration', 'peak_intensity', 'event_severity_index',
            'regional_avg_pm25', 'deviation_from_regional_avg', 'regional_rank', 'is_regional_hotspot',
            'policy_period', 'special_event_flag', 'aqi_category',
            'exceedance_flag_35', 'exceedance_flag_75',
            'cumulative_exposure_7d', 'cumulative_exposure_30d', 'cumulative_exposure_365d', 'exceedance_burden_365d'
        ]
        
        missing_features = [f for f in expected_features if f not in df.columns]
        validation_results['feature_completeness'] = {
            'expected_features': len(expected_features),
            'actual_features': len(df.columns),
            'missing_features': missing_features
        }
        
        # 5. 数据质量标志统计
        quality_flag_stats = df['data_quality_flag'].value_counts().to_dict()
        validation_results['quality_flags'] = quality_flag_stats
        
        print(f"✓ 基础信息: {validation_results['basic_info']['total_records']}条记录, {validation_results['basic_info']['total_features']}个特征")
        print(f"✓ 缺失值: {validation_results['missing_values']['total_missing']}个, 缺失率{validation_results['missing_values']['missing_rate']:.2f}%")
        print(f"✓ 特征完整性: {validation_results['feature_completeness']['actual_features']}/{validation_results['feature_completeness']['expected_features']}个特征")
        
        return validation_results
    
    def create_time_series_visualization(self, df):
        """
        创建时间序列可视化
        
        Args:
            df: 特征数据框
        """
        print("\n=== 创建时间序列可视化 ===")
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. 主要城市PM2.5浓度时间序列
        ax1 = axes[0, 0]
        main_cities = ['北京市', '天津市', '石家庄市', '保定市']
        for city in main_cities:
            city_data = df[df['city'] == city].sort_values('date')
            ax1.plot(city_data['date'], city_data['pm25'], label=city, alpha=0.7)
        
        ax1.set_title('主要城市PM2.5浓度时间序列', fontsize=14, fontweight='bold')
        ax1.set_xlabel('日期')
        ax1.set_ylabel('PM2.5浓度 (μg/m³)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. 月度平均浓度对比
        ax2 = axes[0, 1]
        monthly_avg = df.groupby(['city', 'month'])['pm25'].mean().unstack()
        monthly_avg.T.plot(kind='bar', ax=ax2, width=0.8)
        ax2.set_title('各城市月度平均PM2.5浓度', fontsize=14, fontweight='bold')
        ax2.set_xlabel('月份')
        ax2.set_ylabel('平均浓度 (μg/m³)')
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # 3. 季节性变化
        ax3 = axes[1, 0]
        season_avg = df.groupby(['city', 'season'])['pm25'].mean().unstack()
        season_labels = {1: '春季', 2: '夏季', 3: '秋季', 4: '冬季'}
        season_avg.columns = [season_labels.get(col, col) for col in season_avg.columns]
        season_avg.T.plot(kind='bar', ax=ax3, width=0.8)
        ax3.set_title('各城市季节性PM2.5浓度变化', fontsize=14, fontweight='bold')
        ax3.set_xlabel('季节')
        ax3.set_ylabel('平均浓度 (μg/m³)')
        ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # 4. 年度趋势
        ax4 = axes[1, 1]
        yearly_avg = df.groupby(['city', 'year'])['pm25'].mean().unstack()
        for city in main_cities:
            if city in yearly_avg.columns:
                ax4.plot(yearly_avg.index, yearly_avg[city], marker='o', label=city, linewidth=2)
        
        ax4.set_title('主要城市年度PM2.5浓度趋势', fontsize=14, fontweight='bold')
        ax4.set_xlabel('年份')
        ax4.set_ylabel('平均浓度 (μg/m³)')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        output_path = self.output_dir / 'time_series_analysis.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ 时间序列可视化已保存至: {output_path}")
        plt.close()
    
    def create_spatial_visualization(self, df):
        """
        创建空间分布可视化
        
        Args:
            df: 特征数据框
        """
        print("\n=== 创建空间分布可视化 ===")
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. 各城市平均浓度对比
        ax1 = axes[0, 0]
        city_avg = df.groupby('city')['pm25'].mean().sort_values(ascending=False)
        city_avg.plot(kind='barh', ax=ax1, color='steelblue')
        ax1.set_title('各城市平均PM2.5浓度对比', fontsize=14, fontweight='bold')
        ax1.set_xlabel('平均浓度 (μg/m³)')
        ax1.grid(True, alpha=0.3, axis='x')
        
        # 2. 区域排名分布
        ax2 = axes[0, 1]
        rank_data = df['regional_rank'].value_counts().sort_index()
        rank_data.plot(kind='bar', ax=ax2, color='coral')
        ax2.set_title('区域排名分布', fontsize=14, fontweight='bold')
        ax2.set_xlabel('排名')
        ax2.set_ylabel('天数')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # 3. 偏离区域均值程度
        ax3 = axes[1, 0]
        deviation_data = df.groupby('city')['deviation_from_regional_avg'].mean().sort_values()
        deviation_data.plot(kind='barh', ax=ax3, color='lightgreen')
        ax3.set_title('各城市偏离区域均值程度', fontsize=14, fontweight='bold')
        ax3.set_xlabel('偏离程度 (%)')
        ax3.axvline(x=0, color='red', linestyle='--', linewidth=2)
        ax3.grid(True, alpha=0.3, axis='x')
        
        # 4. 热点城市分布
        ax4 = axes[1, 1]
        hotspot_count = df[df['is_regional_hotspot'] == 1].groupby('city').size().sort_values(ascending=False)
        hotspot_count.plot(kind='bar', ax=ax4, color='orange')
        ax4.set_title('区域热点城市分布', fontsize=14, fontweight='bold')
        ax4.set_xlabel('城市')
        ax4.set_ylabel('热点天数')
        ax4.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        output_path = self.output_dir / 'spatial_analysis.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ 空间分布可视化已保存至: {output_path}")
        plt.close()
    
    def create_policy_effect_visualization(self, df):
        """
        创建政策效果可视化
        
        Args:
            df: 特征数据框
        """
        print("\n=== 创建政策效果可视化 ===")
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. 政策时期平均浓度对比
        ax1 = axes[0, 0]
        policy_avg = df.groupby('policy_period')['pm25'].mean().sort_values()
        policy_avg.plot(kind='barh', ax=ax1, color='skyblue')
        ax1.set_title('各政策时期平均PM2.5浓度', fontsize=14, fontweight='bold')
        ax1.set_xlabel('平均浓度 (μg/m³)')
        ax1.grid(True, alpha=0.3, axis='x')
        
        # 2. 年度趋势对比
        ax2 = axes[0, 1]
        yearly_policy_avg = df.groupby(['year', 'policy_period'])['pm25'].mean().unstack()
        for period in yearly_policy_avg.columns:
            ax2.plot(yearly_policy_avg.index, yearly_policy_avg[period], 
                    marker='o', label=period, linewidth=2)
        ax2.set_title('不同政策时期年度趋势对比', fontsize=14, fontweight='bold')
        ax2.set_xlabel('年份')
        ax2.set_ylabel('平均浓度 (μg/m³)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. AQI等级分布对比
        ax3 = axes[1, 0]
        aqi_policy_dist = pd.crosstab(df['policy_period'], df['aqi_category'])
        aqi_policy_dist.plot(kind='bar', ax=ax3, stacked=True, figsize=(12, 6))
        ax3.set_title('各政策时期AQI等级分布', fontsize=14, fontweight='bold')
        ax3.set_xlabel('政策时期')
        ax3.set_ylabel('天数')
        ax3.legend(title='AQI等级', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # 4. 超标率对比
        ax4 = axes[1, 1]
        exceedance_policy = df.groupby('policy_period')['exceedance_flag_35'].mean() * 100
        exceedance_policy.plot(kind='bar', ax=ax4, color='lightcoral')
        ax4.set_title('各政策时期超标率对比', fontsize=14, fontweight='bold')
        ax4.set_xlabel('政策时期')
        ax4.set_ylabel('超标率 (%)')
        ax4.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        output_path = self.output_dir / 'policy_effect_analysis.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ 政策效果可视化已保存至: {output_path}")
        plt.close()
    
    def create_pollution_event_visualization(self, df):
        """
        创建污染事件可视化
        
        Args:
            df: 特征数据框
        """
        print("\n=== 创建污染事件可视化 ===")
        
        event_data = df[~df['pollution_event_id'].isna()].copy()
        
        if len(event_data) == 0:
            print("⚠ 没有污染事件数据")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. 污染事件数量分布
        ax1 = axes[0, 0]
        event_count = event_data['pollution_event_id'].value_counts()
        event_duration = event_data.groupby('pollution_event_id')['event_duration'].first()
        
        duration_dist = event_duration.value_counts().sort_index()
        duration_dist.plot(kind='bar', ax=ax1, color='steelblue')
        ax1.set_title('污染事件持续时间分布', fontsize=14, fontweight='bold')
        ax1.set_xlabel('持续时间 (天)')
        ax1.set_ylabel('事件数量')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # 2. 事件严重性指数分布
        ax2 = axes[0, 1]
        severity_dist = event_data.groupby('pollution_event_id')['event_severity_index'].first()
        ax2.hist(severity_dist, bins=30, color='coral', edgecolor='black')
        ax2.set_title('污染事件严重性指数分布', fontsize=14, fontweight='bold')
        ax2.set_xlabel('严重性指数')
        ax2.set_ylabel('事件数量')
        ax2.grid(True, alpha=0.3)
        
        # 3. 各城市污染事件数量
        ax3 = axes[1, 0]
        city_event_count = event_data.groupby('city')['pollution_event_id'].nunique().sort_values(ascending=False)
        city_event_count.plot(kind='bar', ax=ax3, color='lightgreen')
        ax3.set_title('各城市污染事件数量', fontsize=14, fontweight='bold')
        ax3.set_xlabel('城市')
        ax3.set_ylabel('事件数量')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # 4. 事件峰值强度分布
        ax4 = axes[1, 1]
        peak_dist = event_data.groupby('pollution_event_id')['peak_intensity'].first()
        ax4.hist(peak_dist, bins=30, color='orange', edgecolor='black')
        ax4.set_title('污染事件峰值强度分布', fontsize=14, fontweight='bold')
        ax4.set_xlabel('峰值浓度 (μg/m³)')
        ax4.set_ylabel('事件数量')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        output_path = self.output_dir / 'pollution_event_analysis.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ 污染事件可视化已保存至: {output_path}")
        plt.close()
    
    def create_health_risk_visualization(self, df):
        """
        创建健康风险可视化
        
        Args:
            df: 特征数据框
        """
        print("\n=== 创建健康风险可视化 ===")
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. AQI等级分布
        ax1 = axes[0, 0]
        aqi_dist = df['aqi_category'].value_counts()
        colors = ['green', 'yellow', 'orange', 'red', 'purple', 'brown']
        aqi_dist.plot(kind='pie', ax=ax1, autopct='%1.1f%%', colors=colors, startangle=90)
        ax1.set_title('AQI等级分布', fontsize=14, fontweight='bold')
        
        # 2. 累计暴露量趋势
        ax2 = axes[0, 1]
        main_cities = ['北京市', '天津市', '石家庄市', '保定市']
        for city in main_cities:
            city_data = df[df['city'] == city].sort_values('date')
            ax2.plot(city_data['date'], city_data['cumulative_exposure_30d'], 
                    label=city, alpha=0.7)
        ax2.set_title('主要城市30天累计暴露量趋势', fontsize=14, fontweight='bold')
        ax2.set_xlabel('日期')
        ax2.set_ylabel('累计暴露天数')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. 超标负担对比
        ax3 = axes[1, 0]
        city_burden = df.groupby('city')['exceedance_burden_365d'].mean().sort_values(ascending=False)
        city_burden.plot(kind='barh', ax=ax3, color='lightcoral')
        ax3.set_title('各城市平均超标负担', fontsize=14, fontweight='bold')
        ax3.set_xlabel('超标负担 (μg/m³)')
        ax3.grid(True, alpha=0.3, axis='x')
        
        # 4. 超标率趋势
        ax4 = axes[1, 1]
        yearly_exceedance = df.groupby('year')['exceedance_flag_35'].mean() * 100
        yearly_exceedance.plot(kind='line', ax=ax4, marker='o', linewidth=2, color='steelblue')
        ax4.set_title('年度超标率趋势', fontsize=14, fontweight='bold')
        ax4.set_xlabel('年份')
        ax4.set_ylabel('超标率 (%)')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        output_path = self.output_dir / 'health_risk_analysis.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ 健康风险可视化已保存至: {output_path}")
        plt.close()
    
    def generate_statistical_report(self, df, validation_results):
        """
        生成统计分析报告
        
        Args:
            df: 特征数据框
            validation_results: 数据质量验证结果
        """
        print("\n=== 生成统计分析报告 ===")
        
        report_path = self.output_dir / 'statistical_report.md'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# 京津冀PM2.5数据集统计分析报告\n\n")
            f.write(f"生成时间: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # 1. 数据集概述
            f.write("## 1. 数据集概述\n\n")
            f.write(f"- **总记录数**: {validation_results['basic_info']['total_records']:,} 条\n")
            f.write(f"- **总特征数**: {validation_results['basic_info']['total_features']} 个\n")
            f.write(f"- **时间范围**: {validation_results['basic_info']['time_range'][0].strftime('%Y-%m-%d')} 到 {validation_results['basic_info']['time_range'][1].strftime('%Y-%m-%d')}\n")
            f.write(f"- **覆盖城市**: {validation_results['basic_info']['city_count']} 个\n")
            f.write(f"- **城市列表**: {', '.join(validation_results['basic_info']['cities'])}\n\n")
            
            # 2. 数据质量评估
            f.write("## 2. 数据质量评估\n\n")
            f.write(f"- **缺失值总数**: {validation_results['missing_values']['total_missing']:,} 个\n")
            f.write(f"- **缺失率**: {validation_results['missing_values']['missing_rate']:.4f}%\n")
            f.write(f"- **特征完整性**: {validation_results['feature_completeness']['actual_features']}/{validation_results['feature_completeness']['expected_features']} 个特征\n\n")
            
            # 3. PM2.5浓度统计
            f.write("## 3. PM2.5浓度统计\n\n")
            pm25_stats = df['pm25'].describe()
            f.write(f"- **平均值**: {pm25_stats['mean']:.2f} μg/m³\n")
            f.write(f"- **中位数**: {pm25_stats['50%']:.2f} μg/m³\n")
            f.write(f"- **标准差**: {pm25_stats['std']:.2f} μg/m³\n")
            f.write(f"- **最小值**: {pm25_stats['min']:.2f} μg/m³\n")
            f.write(f"- **最大值**: {pm25_stats['max']:.2f} μg/m³\n")
            f.write(f"- **范围**: {validation_results['data_ranges']['pm25_range'][0]:.2f} - {validation_results['data_ranges']['pm25_range'][1]:.2f} μg/m³\n\n")
            
            # 4. AQI等级分布
            f.write("## 4. AQI等级分布\n\n")
            aqi_dist = df['aqi_category'].value_counts()
            for category, count in aqi_dist.items():
                percentage = count / len(df) * 100
                f.write(f"- **{category}**: {count:,} 天 ({percentage:.1f}%)\n")
            f.write("\n")
            
            # 5. 污染事件统计
            f.write("## 5. 污染事件统计\n\n")
            event_data = df[~df['pollution_event_id'].isna()]
            if len(event_data) > 0:
                f.write(f"- **污染事件总数**: {event_data['pollution_event_id'].nunique():,} 个\n")
                f.write(f"- **涉及城市数**: {event_data['city'].nunique()} 个\n")
                
                event_duration = event_data.groupby('pollution_event_id')['event_duration'].first()
                f.write(f"- **平均持续时间**: {event_duration.mean():.1f} 天\n")
                f.write(f"- **最长持续时间**: {event_duration.max():.0f} 天\n")
                f.write(f"- **最短持续时间**: {event_duration.min():.0f} 天\n")
                
                event_peak = event_data.groupby('pollution_event_id')['peak_intensity'].first()
                f.write(f"- **平均峰值浓度**: {event_peak.mean():.1f} μg/m³\n")
                f.write(f"- **最高峰值浓度**: {event_peak.max():.1f} μg/m³\n")
            f.write("\n")
            
            # 6. 政策效果分析
            f.write("## 6. 政策效果分析\n\n")
            policy_avg = df.groupby('policy_period')['pm25'].agg(['mean', 'std', 'count'])
            for period in policy_avg.index:
                f.write(f"### {period}\n")
                f.write(f"- **平均浓度**: {policy_avg.loc[period, 'mean']:.2f} μg/m³\n")
                f.write(f"- **标准差**: {policy_avg.loc[period, 'std']:.2f} μg/m³\n")
                f.write(f"- **数据量**: {policy_avg.loc[period, 'count']:,} 条\n\n")
            
            # 7. 健康风险评估
            f.write("## 7. 健康风险评估\n\n")
            f.write(f"- **超标率(35μg/m³)**: {(df['exceedance_flag_35'].mean() * 100):.1f}%\n")
            f.write(f"- **超标率(75μg/m³)**: {(df['exceedance_flag_75'].mean() * 100):.1f}%\n")
            
            city_burden = df.groupby('city')['exceedance_burden_365d'].mean()
            f.write(f"- **平均超标负担**: {city_burden.mean():.1f} μg/m³\n")
            f.write(f"- **最高超标负担城市**: {city_burden.idxmax()} ({city_burden.max():.1f} μg/m³)\n")
            f.write(f"- **最低超标负担城市**: {city_burden.idxmin()} ({city_burden.min():.1f} μg/m³)\n\n")
            
            # 8. 创造性特征总结
            f.write("## 8. 创造性特征总结\n\n")
            f.write("### 8.1 时间维度特征\n")
            f.write("- 滑动平均特征(7天、30天)\n")
            f.write("- 趋势分析特征(30天趋势斜率)\n")
            f.write("- 同比变化特征(年际变化百分比)\n")
            f.write("- 季节性特征(季节划分)\n\n")
            
            f.write("### 8.2 污染事件特征\n")
            f.write("- 污染事件自动识别算法\n")
            f.write("- 事件持续时间、峰值强度、严重性指数\n")
            f.write("- 事件编号和追踪\n\n")
            
            f.write("### 8.3 空间维度特征\n")
            f.write("- 区域统计特征(平均值、排名)\n")
            f.write("- 偏离程度特征(相对区域均值)\n")
            f.write("- 热点识别算法\n\n")
            
            f.write("### 8.4 政策维度特征\n")
            f.write("- 政策时期自动标注\n")
            f.write("- 重大活动标志\n")
            f.write("- 政策效果量化分析\n\n")
            
            f.write("### 8.5 健康风险维度特征\n")
            f.write("- AQI等级自动分类\n")
            f.write("- 超标标志和累计暴露量\n")
            f.write("- 超标负担计算\n\n")
            
            f.write("## 9. 数据知识产权价值点\n\n")
            f.write("### 9.1 创造性加工\n")
            f.write("- 从单一浓度值数据，通过算法规则创造出多维度新知识\n")
            f.write("- 时间模式识别、空间关系分析、事件识别等智能处理\n")
            f.write("- 政策影响评估、健康风险量化等业务知识融合\n\n")
            
            f.write("### 9.2 应用价值\n")
            f.write("- 支持空气质量预测和预警\n")
            f.write("- 支持政策效果评估和决策\n")
            f.write("- 支持健康风险评估和公共卫生管理\n")
            f.write("- 支持区域联防联控和污染治理\n\n")
            
            f.write("### 9.3 数据质量保证\n")
            f.write("- 完整的数据质量检查和验证\n")
            f.write("- 科学的缺失值处理和插补策略\n")
            f.write("- 严格的数据标准化和质量控制\n")
            f.write("- 可重复的数据处理流程\n\n")
        
        print(f"✓ 统计分析报告已保存至: {report_path}")
    
    def run_full_analysis(self):
        """
        运行完整的数据分析流程
        """
        print("=" * 60)
        print("京津冀PM2.5数据集完整分析流程")
        print("=" * 60)
        
        # 1. 加载数据
        df = self.load_features_data()
        if df is None:
            return None
        
        # 2. 数据质量验证
        validation_results = self.data_quality_validation(df)
        
        # 3. 创建可视化图表
        self.create_time_series_visualization(df)
        self.create_spatial_visualization(df)
        self.create_policy_effect_visualization(df)
        self.create_pollution_event_visualization(df)
        self.create_health_risk_visualization(df)
        
        # 4. 生成统计分析报告
        self.generate_statistical_report(df, validation_results)
        
        print("\n" + "=" * 60)
        print("数据分析流程完成!")
        print("=" * 60)
        print(f"\n所有分析结果已保存至: {self.output_dir}")
        print("\n生成的文件:")
        print("- time_series_analysis.png: 时间序列分析")
        print("- spatial_analysis.png: 空间分布分析")
        print("- policy_effect_analysis.png: 政策效果分析")
        print("- pollution_event_analysis.png: 污染事件分析")
        print("- health_risk_analysis.png: 健康风险分析")
        print("- statistical_report.md: 统计分析报告")
        
        return df

if __name__ == "__main__":
    """
    测试数据分析流程
    """
    print("=" * 60)
    print("测试数据分析流程")
    print("=" * 60)
    
    analyzer = DataAnalyzer()
    result = analyzer.run_full_analysis()
    
    if result is not None:
        print("\n测试完成: 数据分析流程执行成功!")
    else:
        print("\n测试完成: 数据分析流程执行失败!")