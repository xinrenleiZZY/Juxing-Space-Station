#!/usr/bin/env python3
# LSTM分析命令行接口
# 运行方式：python cli.py [command] [options]

import os
import sys
import argparse
import subprocess
import shutil
import pandas as pd


class LSTMCLI:
    """LSTM分析命令行接口类"""
    
    def __init__(self):
        """初始化命令行解析器"""
        self.parser = argparse.ArgumentParser(
            description="🎯 LSTM-PM2.5预测分析系统命令行接口",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
✅ 命令示例：
  python cli.py preprocess          # 运行数据预处理
  python cli.py train               # 训练LSTM模型
  python cli.py evaluate            # 评估模型性能
  python cli.py dashboard           # 启动可视化大屏
  python cli.py run_all             # 运行完整流程
  python cli.py config              # 查看配置信息
  python cli.py clean --all         # 清除所有结果文件
            """
        )
        
        # 创建子命令解析器
        subparsers = self.parser.add_subparsers(dest="command", help="可用命令")
        
        # 1. 数据预处理命令
        preprocess_parser = subparsers.add_parser("preprocess", help="📊 运行数据预处理")
        preprocess_parser.add_argument(
            "--city", type=str, default=None,
            help="选择要处理的城市（默认处理所有城市）"
        )
        preprocess_parser.add_argument(
            "--input", type=str, default="data_preparation",
            help="输入数据目录（默认：data_preparation）"
        )
        
        # 2. 模型训练命令
        train_parser = subparsers.add_parser("train", help="🤖 训练LSTM模型")
        train_parser.add_argument(
            "--epochs", type=int, default=None,
            help="训练轮数（默认使用配置文件）"
        )
        train_parser.add_argument(
            "--batch_size", type=int, default=None,
            help="批量大小（默认使用配置文件）"
        )
        
        # 3. 模型评估命令
        evaluate_parser = subparsers.add_parser("evaluate", help="📈 评估模型性能")
        
        # 4. 可视化大屏命令
        dashboard_parser = subparsers.add_parser("dashboard", help="🎨 启动可视化大屏")
        dashboard_parser.add_argument(
            "--port", type=int, default=None,
            help="指定端口号（默认：8501）"
        )
        
        # 5. 运行完整流程命令
        run_all_parser = subparsers.add_parser("run_all", help="🔄 运行完整流程")
        run_all_parser.add_argument(
            "--city", type=str, default=None,
            help="选择要处理的城市（默认处理所有城市）"
        )
        
        # 6. 查看配置信息命令
        config_parser = subparsers.add_parser("config", help="⚙️ 查看配置信息")
        
        # 7. 清除结果文件命令
        clean_parser = subparsers.add_parser("clean", help="🧹 清除结果文件")
        clean_parser.add_argument(
            "--all", action="store_true",
            help="清除所有结果文件（包括模型、数据和可视化）"
        )
        clean_parser.add_argument(
            "--models", action="store_true",
            help="仅清除模型文件"
        )
        clean_parser.add_argument(
            "--data", action="store_true",
            help="仅清除数据文件"
        )
        clean_parser.add_argument(
            "--visualization", action="store_true",
            help="仅清除可视化文件"
        )
        
        # 8. 查看数据概览命令
        data_parser = subparsers.add_parser("data", help="📋 查看数据概览")
        
    
    def run(self):
        """运行命令行接口"""
        args = self.parser.parse_args()
        
        if not args.command:
            self._usage()
            sys.exit(1)
        
        # 获取当前目录
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        
        try:
            # 执行对应的命令
            if args.command == "preprocess":
                self._run_preprocess(args)
            elif args.command == "train":
                self._run_train(args)
            elif args.command == "evaluate":
                self._run_evaluate(args)
            elif args.command == "dashboard":
                self._run_dashboard(args)
            elif args.command == "run_all":
                self._run_all(args)
            elif args.command == "config":
                self._show_config()
            elif args.command == "clean":
                self._clean_results(args)
            elif args.command == "data":
                self._show_data_info()
            else:
                print(f"❌ 未知命令: {args.command}")
                self._usage()
                sys.exit(1)
                
        except Exception as e:
            print(f"\n❌ 执行失败: {e}")
            sys.exit(1)
    
    def _usage(self):
        """显示使用说明"""
        print("✅ 欢迎使用LSTM-PM2.5预测分析系统！🎯")
        print("🔄 用法: python cli.py [command] [options]")
        print("\n可用命令：")
        print("  preprocess     📊 运行数据预处理")
        print("  train          🤖 训练LSTM模型")
        print("  evaluate       📈 评估模型性能")
        print("  dashboard      🎨 启动可视化大屏")
        print("  run_all        🔄 运行完整流程（预处理→训练→评估）")
        print("  config         ⚙️ 查看配置信息")
        print("  clean          🧹 清除结果文件")
        print("  data           📋 查看数据概览")
        print("\n使用 'python cli.py [command] -h' 查看详细选项")
    
    def _run_preprocess(self, args):
        """运行数据预处理"""
        print("📊 正在运行数据预处理...")
        
        preprocess_script = os.path.join(self.current_dir, "data_processing", "data_processing.py")
        
        if not os.path.exists(preprocess_script):
            print("❌ 错误：数据预处理脚本不存在")
            sys.exit(1)
        
        # 构建命令参数
        cmd = [sys.executable, preprocess_script]
        if args.city:
            cmd.extend(["--city", args.city])
        
        # 运行数据预处理脚本
        subprocess.run(cmd, check=True, cwd=self.current_dir)
        print("✅ 数据预处理完成！")
    
    def _run_train(self, args):
        """训练LSTM模型"""
        print("🤖 正在训练LSTM模型...")
        
        train_script = os.path.join(self.current_dir, "model_training", "train_model.py")
        
        if not os.path.exists(train_script):
            print("❌ 错误：模型训练脚本不存在")
            sys.exit(1)
        
        # 构建命令参数
        cmd = [sys.executable, train_script]
        
        # 运行模型训练脚本
        subprocess.run(cmd, check=True, cwd=self.current_dir)
        print("✅ 模型训练完成！")
    
    def _run_evaluate(self, args):
        """评估模型性能"""
        print("📈 正在评估模型性能...")
        
        evaluate_script = os.path.join(self.current_dir, "model_evaluation", "evaluate_model.py")
        
        if not os.path.exists(evaluate_script):
            print("❌ 错误：模型评估脚本不存在")
            sys.exit(1)
        
        # 运行模型评估脚本
        subprocess.run([sys.executable, evaluate_script], check=True, cwd=self.current_dir)
        print("✅ 模型评估完成！")
    
    def _run_dashboard(self, args):
        """启动可视化大屏"""
        print("🎨 正在启动可视化大屏...")
        
        dashboard_script = os.path.join(self.current_dir, "visualization_dashboard.py")
        
        if not os.path.exists(dashboard_script):
            print("❌ 错误：可视化大屏脚本不存在")
            sys.exit(1)
        
        # 构建命令参数
        cmd = [sys.executable, "-m", "streamlit", "run", dashboard_script]
        if args.port:
            cmd.extend(["--server.port", str(args.port)])
        
        print("🌐 应用将在浏览器中打开")
        print("📝 按 Ctrl+C 可终止应用")
        print("\n" + "-" * 50)
        
        # 启动Streamlit服务器
        try:
            subprocess.run(cmd, check=True, cwd=self.current_dir)
        except KeyboardInterrupt:
            print("\n\n🔌 应用已终止")
    
    def _run_all(self, args):
        """运行完整流程"""
        print("🔄 正在运行完整流程...")
        print("\n" + "=" * 50)
        
        # 1. 数据预处理
        print("📊 1. 数据预处理")
        self._run_preprocess(args)
        print("=" * 50)
        
        # 2. 模型训练
        print("🤖 2. 模型训练")
        self._run_train(args)
        print("=" * 50)
        
        # 3. 模型评估
        print("📈 3. 模型评估")
        self._run_evaluate(args)
        print("=" * 50)
        
        print("✅ 完整流程运行完成！")
        print("🎨 可以运行 'python cli.py dashboard' 查看可视化结果")
    
    def _show_config(self):
        """查看配置信息"""
        print("⚙️ LSTM分析系统配置信息")
        print("-" * 50)
        
        # 读取配置文件
        config_path = os.path.join(self.current_dir, "configs", "config.py")
        
        if not os.path.exists(config_path):
            print("❌ 错误：配置文件不存在")
            return
        
        with open(config_path, "r", encoding="utf-8") as f:
            config_content = f.read()
        
        # 提取关键配置信息
        print("📋 主要配置参数：")
        for line in config_content.split("\n"):
            if line.strip() and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().split("#")[0].strip()
                if value:
                    print(f"  {key:<20} = {value}")
    
    def _clean_results(self, args):
        """清除结果文件"""
        print("🧹 正在清除结果文件...")
        
        # 定义要清除的目录和文件
        results_dir = os.path.join(self.current_dir, "results")
        visualization_dir = os.path.join(self.current_dir, "visualization")
        
        # 清除所有文件
        if args.all:
            self._clean_dir(results_dir, keep_empty=False)
            self._clean_dir(visualization_dir, keep_empty=False)
            print("✅ 已清除所有结果文件")
            return
        
        # 仅清除结果数据
        if args.data:
            self._clean_dir(results_dir, keep_empty=False)
            print("✅ 已清除结果数据文件")
        
        # 仅清除模型文件
        if args.models:
            if os.path.exists(results_dir):
                model_files = [f for f in os.listdir(results_dir) if f.endswith(".h5")]
                for file in model_files:
                    os.remove(os.path.join(results_dir, file))
                print(f"✅ 已清除 {len(model_files)} 个模型文件")
        
        # 仅清除可视化文件
        if args.visualization:
            self._clean_dir(visualization_dir, keep_empty=False)
            print("✅ 已清除可视化结果文件")
        
        # 如果没有指定任何选项
        if not any([args.all, args.models, args.data, args.visualization]):
            print("📝 请指定要清除的内容：--all, --models, --data, --visualization")
    
    def _clean_dir(self, dir_path, keep_empty=True):
        """清除目录中的所有文件"""
        if os.path.exists(dir_path):
            for file_name in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            if not keep_empty:
                os.rmdir(dir_path)
    
    def _show_data_info(self):
        """查看数据概览"""
        print("📋 数据概览")
        print("-" * 50)
        
        # 检查预处理数据
        preprocessed_file = os.path.join(self.current_dir, "results", "full_preprocessed_data.csv")
        
        if os.path.exists(preprocessed_file):
            df = pd.read_csv(preprocessed_file)
            print(f"📊 预处理数据：")
            print(f"  总记录数: {len(df):,}")
            print(f"  包含城市: {', '.join(df['城市'].unique())}")
            print(f"  日期范围: {df['日期'].min()} 至 {df['日期'].max()}")
            print(f"  特征列数: {len(df.columns)}")
            print()
        else:
            print("❌ 预处理数据文件不存在，请先运行 'python cli.py preprocess'")
            print()
        
        # 检查原始数据
        data_prep_dir = os.path.join(self.current_dir, "data_preparation")
        if os.path.exists(data_prep_dir):
            csv_files = [f for f in os.listdir(data_prep_dir) if f.endswith(".csv")]
            if csv_files:
                print(f"📁 原始数据文件：")
                for file in csv_files:
                    file_path = os.path.join(data_prep_dir, file)
                    try:
                        df = pd.read_csv(file_path)
                        print(f"  - {file}: {len(df):,} 条记录")
                    except Exception:
                        print(f"  - {file}: 无法读取")
        
        # 检查结果文件
        results_dir = os.path.join(self.current_dir, "results")
        if os.path.exists(results_dir):
            result_files = os.listdir(results_dir)
            if result_files:
                print(f"\n📋 结果文件：")
                for file in result_files:
                    file_path = os.path.join(results_dir, file)
                    size_mb = os.path.getsize(file_path) / (1024 * 1024)
                    print(f"  - {file}: {size_mb:.2f} MB")


if __name__ == "__main__":
    cli = LSTMCLI()
    cli.run()
