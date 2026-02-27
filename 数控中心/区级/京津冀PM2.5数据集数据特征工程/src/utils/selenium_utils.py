from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from src.utils.logger import setup_logger
from config.settings import USER_AGENT_POOL, PROXY_POOL, USE_PROXY, TUNNEL_PROXY, USE_TUNNEL_PROXY, BASE_DIR
import os
import random
import time
import logging
from fake_useragent import UserAgent
# 初始化日志对象
logger = setup_logger(__name__)  # 关键修复：定义logger变量

def create_chrome_driver():
    """创建配置好的Chrome驱动（反爬+SSL忽略）"""
    chrome_options = Options()
    
    # 基础配置
    # chrome_options.add_argument("--headless=new")  # 无头模式（可选）
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--ignore-certificate-errors")
    
    # 忽略SSL证书错误
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-insecure-localhost")
    
    # 隐藏webdriver特征(隐藏自动化特征)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    # 随机User-Agent（使用fake_useragent增强随机性）
    ua = UserAgent()
    random_ua = random.choice([ua.chrome, ua.firefox, ua.safari])
    chrome_options.add_argument(f"user-agent={random_ua}")

    # 随机代理（Selenium版）
    if USE_PROXY and PROXY_POOL:
        proxy = random.choice(PROXY_POOL).split("//")[-1]  # 提取IP:端口
        chrome_options.add_argument(f"--proxy-server={proxy}")
        logger.info(f"Selenium使用代理：{proxy}")

    # 添加隧道代理
    if USE_TUNNEL_PROXY:
        tunnel = TUNNEL_PROXY["tunnel"]
        username = TUNNEL_PROXY["username"]
        password = TUNNEL_PROXY["password"]
        # Selenium代理格式：--proxy-server=http://user:pass@host:port
        proxy_arg = f"--proxy-server=https://{username}:{password}@{tunnel}"
        chrome_options.add_argument(proxy_arg)
        print(f"Selenium已启用隧道代理：{tunnel}")

    # 随机窗口大小
    chrome_options.add_argument(f"--window-size={random.randint(1024, 1280)},{random.randint(768, 900)}")
    
    # 禁用浏览器提示
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")

    # 驱动路径（优先手动指定，失败则自动下载）
    driver_path = os.path.join(BASE_DIR, "chromedriver.exe")
    try:
        # 检查手动路径是否存在
        if os.path.exists(driver_path):
            service = Service(executable_path=driver_path)
            logger.info(f"使用手动指定的ChromeDriver：{driver_path}")
        else:
            raise FileNotFoundError(f"未找到手动配置的驱动：{driver_path}")
    except Exception as e:
        logger.warning(f"手动驱动加载失败，尝试自动下载：{str(e)}")
        service = Service(ChromeDriverManager().install())

    # 初始化驱动
    driver = webdriver.Chrome(
        service=service,
        options=chrome_options
    )
    
    # 进一步隐藏自动化特征
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
            Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh']});
        """
    })

    # 随机隐式等待
    driver.implicitly_wait(random.uniform(2, 5))

    return driver