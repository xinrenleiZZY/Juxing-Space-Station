#!/usr/bin/env python3
# PM2.5预测可视化大屏 - 主入口文件
# 运行方式：python dashboard.py

import os
import sys
import subprocess


def main():
    """主入口函数"""
    print("🚀 正在启动PM2.5预测可视化大屏...")
    
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 检查依赖
    check_dependencies()
    
    # 启动Streamlit应用
    dashboard_file = os.path.join(current_dir, "visualization_dashboard.py")
    
    if not os.path.exists(dashboard_file):
        print("❌ 错误：可视化大屏文件不存在")
        sys.exit(1)
    
    print("📊 正在启动可视化大屏...")
    print("🌐 应用将在浏览器中打开")
    print("📝 按 Ctrl+C 可终止应用")
    print("\n" + "-" * 50)
    
    # 启动Streamlit服务器
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", dashboard_file],
            check=True,
            cwd=current_dir
        )
    except KeyboardInterrupt:
        print("\n\n🔌 应用已终止")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 启动失败：{e}")
        sys.exit(1)


def check_dependencies():
    """检查关键依赖是否安装"""
    print("🔍 正在检查依赖...")
    
    required_packages = [
        "streamlit",
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "tensorflow",
        "sklearn",  # 使用sklearn而不是scikit-learn进行导入
        "joblib"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} 已安装")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} 未安装")
    
    if missing_packages:
        print("\n📦 建议安装缺失的依赖：")
        # 将sklearn转换为scikit-learn用于安装
        install_packages = []
        for pkg in missing_packages:
            if pkg == "sklearn":
                install_packages.append("scikit-learn")
            else:
                install_packages.append(pkg)
        print(f"pip install {' '.join(install_packages)}")
        print("\n" + "-" * 50)


if __name__ == "__main__":
    main()
