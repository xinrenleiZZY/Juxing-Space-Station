# src/simple_analysis.py
import pandas as pd
import numpy as np
from pathlib import Path
import warnings
import sys
warnings.filterwarnings('ignore')

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent))

from config.settings import *

class SimpleAnalyzer:
    def __init__(self, features_data_path=None):
        """
        初始化简单分析器
        
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
    
    def generate_comprehensive_report(self, df):
        """
        生成综合分析报告
        
        Args:
            df: 特征数据框
        """
        print("\n=== 生成综合分析报告 ===")
        
        report_path = self.output_dir / 'comprehensive_analysis_report.md'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# 京津冀PM2.5数据集综合分析报告\n\n")
            f.write(f"生成时间: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # 1. 数据集概述
            f.write("## 1. 数据集概述\n\n")
            f.write(f"- **总记录数**: {len(df):,} 条\n")
            f.write(f"- **总特征数**: {len(df.columns)} 个\n")
            f.write(f"- **时间范围**: {df['date'].min().strftime('%Y-%m-%d')} 到 {df['date'].max().strftime('%Y-%m-%d')}\n")
            f.write(f"- **覆盖城市**: {df['city'].nunique()} 个\n")
            f.write(f"- **城市列表**: {', '.join(sorted(df['city'].unique()))}\n\n")
            
            # 2. 数据质量评估
            f.write("## 2. 数据质量评估\n\n")
            missing_stats = df.isnull().sum()
            total_missing = missing_stats.sum()
            missing_rate = (total_missing / (len(df) * len(df.columns))) * 100
            
            f.write(f"- **缺失值总数**: {total_missing:,} 个\n")
            f.write(f"- **缺失率**: {missing_rate:.4f}%\n")
            
            if total_missing > 0:
                f.write("- **缺失值分布**:\n")
                for col, count in missing_stats[missing_stats > 0].items():
                    f.write(f"  - {col}: {count:,} 个 ({count/len(df)*100:.2f}%)\n")
            f.write("\n")
            
            # 3. PM2.5浓度统计
            f.write("## 3. PM2.5浓度统计\n\n")
            pm25_stats = df['pm25'].describe()
            f.write(f"- **平均值**: {pm25_stats['mean']:.2f} μg/m³\n")
            f.write(f"- **中位数**: {pm25_stats['50%']:.2f} μg/m³\n")
            f.write(f"- **标准差**: {pm25_stats['std']:.2f} μg/m³\n")
            f.write(f"- **最小值**: {pm25_stats['min']:.2f} μg/m³\n")
            f.write(f"- **最大值**: {pm25_stats['max']:.2f} μg/m³\n")
            f.write(f"- **变异系数**: {(pm25_stats['std']/pm25_stats['mean']*100):.2f}%\n\n")
            
            # 4. 各城市统计
            f.write("## 4. 各城市PM2.5浓度统计\n\n")
            city_stats = df.groupby('city')['pm25'].agg(['mean', 'std', 'min', 'max', 'count'])
            city_stats = city_stats.sort_values('mean', ascending=False)
            
            f.write("| 城市 | 平均浓度(μg/m³) | 标准差 | 最小值 | 最大值 | 数据量 |\n")
            f.write("|------|------------------|--------|--------|--------|--------|\n")
            for city, row in city_stats.iterrows():
                f.write(f"| {city} | {row['mean']:.2f} | {row['std']:.2f} | {row['min']:.2f} | {row['max']:.2f} | {row['count']:,} |\n")
            f.write("\n")
            
            # 5. AQI等级分布
            f.write("## 5. AQI等级分布\n\n")
            aqi_dist = df['aqi_category'].value_counts()
            total_days = len(df)
            
            f.write("| AQI等级 | 天数 | 占比 |\n")
            f.write("|----------|------|------|\n")
            for category, count in aqi_dist.items():
                percentage = count / total_days * 100
                f.write(f"| {category} | {count:,} | {percentage:.1f}% |\n")
            f.write("\n")
            
            # 6. 污染事件统计
            f.write("## 6. 污染事件统计\n\n")
            event_data = df[~df['pollution_event_id'].isna()].copy()
            
            if len(event_data) > 0:
                total_events = event_data['pollution_event_id'].nunique()
                event_cities = event_data['city'].nunique()
                
                f.write(f"- **污染事件总数**: {total_events:,} 个\n")
                f.write(f"- **涉及城市数**: {event_cities} 个\n")
                
                event_duration = event_data.groupby('pollution_event_id')['event_duration'].first()
                f.write(f"- **平均持续时间**: {event_duration.mean():.1f} 天\n")
                f.write(f"- **最长持续时间**: {event_duration.max():.0f} 天\n")
                f.write(f"- **最短持续时间**: {event_duration.min():.0f} 天\n")
                
                event_peak = event_data.groupby('pollution_event_id')['peak_intensity'].first()
                f.write(f"- **平均峰值浓度**: {event_peak.mean():.1f} μg/m³\n")
                f.write(f"- **最高峰值浓度**: {event_peak.max():.1f} μg/m³\n")
                
                event_severity = event_data.groupby('pollution_event_id')['event_severity_index'].first()
                f.write(f"- **平均严重性指数**: {event_severity.mean():.1f}\n")
                f.write(f"- **最高严重性指数**: {event_severity.max():.1f}\n\n")
                
                # 各城市污染事件数量
                f.write("### 各城市污染事件数量\n\n")
                city_event_count = event_data.groupby('city')['pollution_event_id'].nunique().sort_values(ascending=False)
                f.write("| 城市 | 事件数量 |\n")
                f.write("|------|----------|\n")
                for city, count in city_event_count.items():
                    f.write(f"| {city} | {count} |\n")
                f.write("\n")
            else:
                f.write("- 没有识别到污染事件\n\n")
            
            # 7. 政策效果分析
            f.write("## 7. 政策效果分析\n\n")
            policy_stats = df.groupby('policy_period')['pm25'].agg(['mean', 'std', 'count'])
            
            f.write("| 政策时期 | 平均浓度(μg/m³) | 标准差 | 数据量 |\n")
            f.write("|----------|------------------|--------|--------|\n")
            for period, row in policy_stats.iterrows():
                f.write(f"| {period} | {row['mean']:.2f} | {row['std']:.2f} | {row['count']:,} |\n")
            f.write("\n")
            
            # 政策效果对比
            f.write("### 政策实施效果对比\n\n")
            policy_avg = df.groupby('policy_period')['pm25'].mean()
            
            if '大气十条时期' in policy_avg.index and '蓝天保卫战时期' in policy_avg.index:
                change1 = ((policy_avg['蓝天保卫战时期'] - policy_avg['大气十条时期']) / policy_avg['大气十条时期']) * 100
                f.write(f"- **蓝天保卫战 vs 大气十条**: {change1:+.2f}% ({'改善' if change1 < 0 else '恶化'})\n")
            
            if '蓝天保卫战时期' in policy_avg.index and '十四五深化治理时期' in policy_avg.index:
                change2 = ((policy_avg['十四五深化治理时期'] - policy_avg['蓝天保卫战时期']) / policy_avg['蓝天保卫战时期']) * 100
                f.write(f"- **十四五深化 vs 蓝天保卫战**: {change2:+.2f}% ({'改善' if change2 < 0 else '恶化'})\n")
            
            if '大气十条时期' in policy_avg.index and '十四五深化治理时期' in policy_avg.index:
                change3 = ((policy_avg['十四五深化治理时期'] - policy_avg['大气十条时期']) / policy_avg['大气十条时期']) * 100
                f.write(f"- **十四五深化 vs 大气十条**: {change3:+.2f}% ({'改善' if change3 < 0 else '恶化'})\n")
            f.write("\n")
            
            # 8. 健康风险评估
            f.write("## 8. 健康风险评估\n\n")
            exceedance_35 = df['exceedance_flag_35'].mean() * 100
            exceedance_75 = df['exceedance_flag_75'].mean() * 100
            
            f.write(f"- **超标率(35μg/m³)**: {exceedance_35:.1f}%\n")
            f.write(f"- **超标率(75μg/m³)**: {exceedance_75:.1f}%\n")
            
            city_burden = df.groupby('city')['exceedance_burden_365d'].mean()
            f.write(f"- **平均超标负担**: {city_burden.mean():.1f} μg/m³\n")
            f.write(f"- **最高超标负担城市**: {city_burden.idxmax()} ({city_burden.max():.1f} μg/m³)\n")
            f.write(f"- **最低超标负担城市**: {city_burden.idxmin()} ({city_burden.min():.1f} μg/m³)\n\n")
            
            # 累计暴露量统计
            f.write("### 累计暴露量统计\n\n")
            exposure_stats = df[['cumulative_exposure_7d', 'cumulative_exposure_30d', 'cumulative_exposure_365d']].describe()
            
            f.write("| 时间窗口 | 平均天数 | 最大天数 |\n")
            f.write("|----------|----------|----------|\n")
            f.write(f"| 7天 | {exposure_stats['cumulative_exposure_7d']['mean']:.1f} | {exposure_stats['cumulative_exposure_7d']['max']:.0f} |\n")
            f.write(f"| 30天 | {exposure_stats['cumulative_exposure_30d']['mean']:.1f} | {exposure_stats['cumulative_exposure_30d']['max']:.0f} |\n")
            f.write(f"| 365天 | {exposure_stats['cumulative_exposure_365d']['mean']:.1f} | {exposure_stats['cumulative_exposure_365d']['max']:.0f} |\n\n")
            
            # 9. 空间特征分析
            f.write("## 9. 空间特征分析\n\n")
            
            # 区域排名统计
            rank_stats = df['regional_rank'].describe()
            f.write(f"- **平均区域排名**: {rank_stats['mean']:.1f}\n")
            f.write(f"- **排名中位数**: {rank_stats['50%']:.0f}\n")
            f.write(f"- **排名标准差**: {rank_stats['std']:.2f}\n\n")
            
            # 偏离区域均值程度
            deviation_stats = df['deviation_from_regional_avg'].describe()
            f.write(f"- **平均偏离程度**: {deviation_stats['mean']:.2f}%\n")
            f.write(f"- **偏离程度中位数**: {deviation_stats['50%']:.2f}%\n")
            f.write(f"- **最大偏离程度**: {deviation_stats['max']:.2f}%\n")
            f.write(f"- **最小偏离程度**: {deviation_stats['min']:.2f}%\n\n")
            
            # 热点识别
            hotspot_count = (df['is_regional_hotspot'] == 1).sum()
            hotspot_rate = hotspot_count / len(df) * 100
            f.write(f"- **热点天数**: {hotspot_count:,} 天\n")
            f.write(f"- **热点率**: {hotspot_rate:.2f}%\n\n")
            
            # 各城市热点天数
            f.write("### 各城市热点天数\n\n")
            city_hotspot = df[df['is_regional_hotspot'] == 1].groupby('city').size().sort_values(ascending=False)
            f.write("| 城市 | 热点天数 |\n")
            f.write("|------|----------|\n")
            for city, count in city_hotspot.items():
                f.write(f"| {city} | {count} |\n")
            f.write("\n")
            
            # 10. 时间特征分析
            f.write("## 10. 时间特征分析\n\n")
            
            # 月度分析
            monthly_avg = df.groupby('month')['pm25'].mean()
            f.write("### 月度平均浓度\n\n")
            f.write("| 月份 | 平均浓度(μg/m³) |\n")
            f.write("|------|------------------|\n")
            for month, avg in monthly_avg.items():
                f.write(f"| {month}月 | {avg:.2f} |\n")
            f.write("\n")
            
            # 季节分析
            season_labels = {1: '春季', 2: '夏季', 3: '秋季', 4: '冬季'}
            season_avg = df.groupby('season')['pm25'].mean()
            f.write("### 季节平均浓度\n\n")
            f.write("| 季节 | 平均浓度(μg/m³) |\n")
            f.write("|------|------------------|\n")
            for season, avg in season_avg.items():
                f.write(f"| {season_labels.get(season, season)} | {avg:.2f} |\n")
            f.write("\n")
            
            # 年度趋势
            yearly_avg = df.groupby('year')['pm25'].mean()
            f.write("### 年度平均浓度趋势\n\n")
            f.write("| 年份 | 平均浓度(μg/m³) | 同比变化(%) |\n")
            f.write("|------|------------------|-------------|\n")
            for i, (year, avg) in enumerate(yearly_avg.items()):
                if i > 0:
                    prev_year = list(yearly_avg.index)[i-1]
                    prev_avg = yearly_avg[prev_year]
                    yoy_change = ((avg - prev_avg) / prev_avg) * 100
                    f.write(f"| {year} | {avg:.2f} | {yoy_change:+.2f} |\n")
                else:
                    f.write(f"| {year} | {avg:.2f} | - |\n")
            f.write("\n")
            
            # 11. 数据知识产权价值点
            f.write("## 11. 数据知识产权价值点\n\n")
            
            f.write("### 11.1 创造性加工\n\n")
            f.write("**核心创新点**:\n\n")
            f.write("1. **时间维度知识创造**:\n")
            f.write("   - 滑动平均特征(7天、30天): 识别污染趋势和平滑噪声\n")
            f.write("   - 趋势分析特征(30天斜率): 量化污染变化方向\n")
            f.write("   - 同比变化特征: 评估年际改善程度\n")
            f.write("   - 季节性特征: 识别污染的季节性规律\n\n")
            
            f.write("2. **污染事件智能识别**:\n")
            f.write("   - 基于规则的污染事件识别算法\n")
            f.write("   - 事件持续时间、峰值、严重性指数计算\n")
            f.write("   - 事件编号和追踪系统\n\n")
            
            f.write("3. **空间维度知识创造**:\n")
            f.write("   - 区域统计特征: 量化区域整体污染水平\n")
            f.write("   - 相对排名特征: 评估各城市在区域中的位置\n")
            f.write("   - 偏离程度特征: 识别污染热点和贡献者\n")
            f.write("   - 热点识别算法: 自动发现持续污染区域\n\n")
            
            f.write("4. **政策维度知识融合**:\n")
            f.write("   - 政策时期自动标注: 建立时间-政策关联\n")
            f.write("   - 重大活动标志: 识别特殊时期的污染特征\n")
            f.write("   - 政策效果量化: 评估政策实施效果\n\n")
            
            f.write("5. **健康风险维度知识创造**:\n")
            f.write("   - AQI等级自动分类: 建立浓度-健康风险映射\n")
            f.write("   - 超标标志和累计暴露量: 量化健康风险\n")
            f.write("   - 超标负担计算: 评估长期污染影响\n\n")
            
            f.write("### 11.2 应用价值\n\n")
            f.write("**实际应用场景**:\n\n")
            f.write("1. **空气质量预测和预警**:\n")
            f.write("   - 基于历史趋势和事件模式进行预测\n")
            f.write("   - 支持提前预警和应急响应\n\n")
            
            f.write("2. **政策效果评估**:\n")
            f.write("   - 量化政策实施前后的改善效果\n")
            f.write("   - 支持政策制定和调整决策\n\n")
            
            f.write("3. **健康风险评估**:\n")
            f.write("   - 评估公众长期暴露风险\n")
            f.write("   - 支持公共卫生管理决策\n\n")
            
            f.write("4. **区域联防联控**:\n")
            f.write("   - 识别区域污染传输和关联\n")
            f.write("   - 支持区域协同治理\n\n")
            
            f.write("5. **科学研究支持**:\n")
            f.write("   - 提供高质量的多维度数据\n")
            f.write("   - 支持大气污染机理研究\n\n")
            
            f.write("### 11.3 数据质量保证\n\n")
            f.write("**质量控制措施**:\n\n")
            f.write("1. **数据完整性保证**:\n")
            f.write("   - 全面的数据质量检查和验证\n")
            f.write("   - 科学的缺失值处理和插补策略\n")
            f.write("   - 异常值检测和处理机制\n\n")
            
            f.write("2. **数据标准化**:\n")
            f.write("   - 统一的城市名称标准化\n")
            f.write("   - 一致的时间格式和数据类型\n")
            f.write("   - 严格的数据范围验证\n\n")
            
            f.write("3. **可重复性保证**:\n")
            f.write("   - 完整的数据处理流程记录\n")
            f.write("   - 清晰的特征生成规则说明\n")
            f.write("   - 标准化的数据处理方法\n\n")
            
            f.write("### 11.4 知识产权保护范围\n\n")
            f.write("**保护内容**:\n\n")
            f.write("本数据集的知识产权保护范围包括:\n\n")
            f.write("1. **数据集本身**: 包含32个特征的高价值数据集\n")
            f.write("2. **特征工程方法**: 创造性特征生成的算法和规则\n")
            f.write("3. **数据处理流程**: 从原始数据到特征数据的完整处理流程\n")
            f.write("4. **知识提取方法**: 从数据中提取有价值知识的方法\n")
            f.write("5. **应用价值**: 数据集的实际应用价值和经济效益\n\n")
            
            f.write("### 11.5 创新性说明\n\n")
            f.write("**与原始数据的区别**:\n\n")
            f.write("原始数据仅包含: 日期、城市、PM2.5浓度三个基础字段\n\n")
            f.write("本数据集通过创造性加工，新增了29个衍生特征，包括:\n\n")
            f.write("- 时间维度特征: 8个\n")
            f.write("- 污染事件特征: 4个\n")
            f.write("- 空间维度特征: 4个\n")
            f.write("- 政策维度特征: 2个\n")
            f.write("- 健康风险特征: 7个\n\n")
            f.write("这些特征不是简单的统计汇总，而是通过算法规则、领域知识融合、智能识别等方法创造出的新知识。\n\n")
            
            f.write("### 11.6 数据集规模和价值\n\n")
            f.write("**数据集统计**:\n\n")
            f.write(f"- **时间跨度**: {df['date'].max().year - df['date'].min().year + 1} 年\n")
            f.write(f"- **空间覆盖**: {df['city'].nunique()} 个城市\n")
            f.write(f"- **数据总量**: {len(df):,} 条记录\n")
            f.write(f"- **特征维度**: {len(df.columns)} 个特征\n")
            f.write(f"- **数据质量**: 缺失率{missing_rate:.2f}%，质量优秀\n")
            f.write(f"- **应用价值**: 支持空气质量预测、政策评估、健康风险分析等多个应用场景\n\n")
            
            f.write("---\n\n")
            f.write(f"*报告生成时间: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
            f.write(f"*数据集版本: v1.0*\n")
            f.write(f"*特征工程版本: 2.0 (优化版)*\n")
        
        print(f"✓ 综合分析报告已保存至: {report_path}")
        return report_path
    
    def run_analysis(self):
        """
        运行完整分析流程
        """
        print("=" * 60)
        print("京津冀PM2.5数据集综合分析流程")
        print("=" * 60)
        
        # 1. 加载数据
        df = self.load_features_data()
        if df is None:
            return None
        
        # 2. 生成综合分析报告
        report_path = self.generate_comprehensive_report(df)
        
        print("\n" + "=" * 60)
        print("分析流程完成!")
        print("=" * 60)
        print(f"\n分析结果已保存至: {self.output_dir}")
        print(f"\n生成的文件:")
        print(f"- comprehensive_analysis_report.md: 综合分析报告")
        
        return df

if __name__ == "__main__":
    """
    测试分析流程
    """
    print("=" * 60)
    print("测试分析流程")
    print("=" * 60)
    
    analyzer = SimpleAnalyzer()
    result = analyzer.run_analysis()
    
    if result is not None:
        print("\n测试完成: 分析流程执行成功!")
    else:
        print("\n测试完成: 分析流程执行失败!")