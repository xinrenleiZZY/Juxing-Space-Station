import sys
import time
from config.settings import REALTIME_CRAWL_INTERVAL


def run_scheduled_realtime():
    """定时运行实时数据爬取（每小时一次，使用配置中的间隔时间）"""
    print(f"🚀 开始定时实时爬取（间隔 {REALTIME_CRAWL_INTERVAL/3600} 小时）...")
    print("⚠️  按 Ctrl+C 停止")
    try: 
        while True:
           # 执行实时爬取
            print(f"\n📊 开始执行实时数据爬取 - {time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 直接调用爬虫逻辑，避免循环导入
            try:
                from src.crawlers.aqi_realtime import AQIRealtimeCrawler
                crawler = AQIRealtimeCrawler()
                crawler.crawl_realtime_batch()
            except Exception as e:
                print(f"无法执行实时爬取：{e}")
                return
            
            print(f"✅ 爬取完成 - {time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 可视化倒计时休眠
            print(f"\n⏳ 开始休眠 {REALTIME_CRAWL_INTERVAL/3600} 小时，剩余时间：")
            for remaining in range(REALTIME_CRAWL_INTERVAL, 0, -1):
                # 计算时分秒
                hours = remaining // 3600
                minutes = (remaining % 3600) // 60
                seconds = remaining % 60
                # 格式化输出（覆盖当前行）
                sys.stdout.write(f"\r    {hours:02d}:{minutes:02d}:{seconds:02d}")
                sys.stdout.flush()
                time.sleep(1)
            
            # 休眠结束后清空倒计时行
            sys.stdout.write("\r" + " " * 20 + "\r")  # 清空倒计时显示
            sys.stdout.flush()
            print("\n🔄 休眠结束，准备下一次爬取...")
    except KeyboardInterrupt:
        # 捕获终止信号，优雅退出
        sys.stdout.write("\r" + " " * 20 + "\r")  # 清空倒计时
        sys.stdout.flush()
        print("\n🛑 定时任务已手动停止")
    except Exception as e:
        sys.stdout.write("\r" + " " * 20 + "\r")
        sys.stdout.flush()
        print(f"\n❌ 定时任务异常终止：{str(e)}")


__all__ = ["run_scheduled_realtime"]