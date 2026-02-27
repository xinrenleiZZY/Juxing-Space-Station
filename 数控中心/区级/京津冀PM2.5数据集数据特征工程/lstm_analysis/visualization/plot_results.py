# 结果可视化脚本
"""一键生成所有可视化结果"""
import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model_evaluation.evaluate_model import evaluate_model

if __name__ == "__main__":
    print("=== 生成可视化结果 ===")
    # 执行评估并生成可视化
    evaluate_model()
    print("\n所有可视化结果已生成至 visualization/ 目录！")