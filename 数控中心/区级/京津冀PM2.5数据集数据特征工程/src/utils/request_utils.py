"""请求工具：封装 `requests` session、重试与安全请求函数。

模块提供 `create_session`, `get_headers`, `safe_get` 等常用方法，用于在爬虫中做统一请求。
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config.settings import MAX_RETRY_TIMES, USER_AGENT_POOL, PROXY_POOL, USE_PROXY, PROXY_TIMEOUT, TUNNEL_PROXY, USE_TUNNEL_PROXY
import random
import time
from src.utils.logger import setup_logger
from urllib3.exceptions import InsecureRequestWarning, ProtocolError
import socket
import logging
import ssl
from urllib3.poolmanager import PoolManager

# 忽略SSL验证警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 初始化日志
logger = setup_logger(__name__)


def create_session():
    """创建一个带重试策略的 `requests.Session` 对象。（支持代理）"""
    session = requests.Session()
    retry_strategy = Retry(
        total=MAX_RETRY_TIMES,
        backoff_factor=1,  # 重试间隔：1s, 2s, 4s...
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET","POST"],  # 仅对GET请求重试
        respect_retry_after_header=True  # 尊重服务器的 Retry-After 头
    )
    adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=20, pool_maxsize=20, pool_block=False)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    # 添加隧道代理（仅当启用时）
    if USE_TUNNEL_PROXY:
        tunnel = TUNNEL_PROXY["tunnel"]
        username = TUNNEL_PROXY["username"]
        password = TUNNEL_PROXY["password"]
        # 构造代理格式
        proxy_url = f"http://{username}:{password}@{tunnel}/"
        proxy_urls = f"http://{username}:{password}@{tunnel}/"
        session.proxies = {
            "http": proxy_url,
            "https": proxy_urls
        }
        logger.info(f"已启用隧道代理：{tunnel}")

    return session

def get_random_proxy():
    """从代理池随机选择一个可用代理"""
    if not USE_PROXY or not PROXY_POOL:
        return None
    # 随机打乱代理池顺序
    proxies = random.sample(PROXY_POOL, len(PROXY_POOL))
    for proxy in proxies:
        try:
            # 简单验证代理可用性
            test_url = "http://www.baidu.com"
            res = requests.get(
                test_url, 
                proxies={"http": proxy, "https": proxy},
                timeout=PROXY_TIMEOUT,
                verify=False
            )
            if res.status_code == 200:
                logger.info(f"使用有效代理：{proxy}")
                return {"http": proxy, "https": proxy}
        except Exception:
            logger.warning(f"代理不可用：{proxy}")
            continue
    logger.error("无可用代理，将不使用代理请求")
    return None

def get_headers(referer="https://www.tianqihoubao.com/aqi/"):
    """返回一个与浏览器行为相近的请求头字典（随机 UA）。"""
    # 浏览器UA
    extended_ua = USER_AGENT_POOL + [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    ]
    return {
        "User-Agent": random.choice(extended_ua),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Referer": referer,
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": random.choice(["same-origin", "none"]),
        "Sec-Fetch-User": "?1",
        "TE": "Trailers"
    }


def safe_get(session, url, params=None, timeout=15, referer=None, verify=False):
    """安全请求：集成代理池、动态间隔、自动重试、添加伪装头并返回 response 或 None。

    在底层连接被远端重置（ProtocolError / ConnectionResetError）时，
    会按 `MAX_RETRY_TIMES` 进行指数退避重试，并在每次重试时尝试重建会话以避免复用已损坏的连接。
    """

    # 随机间隔优化（根据域名动态调整间隔）
    domain = url.split("//")[-1].split("/")[0]
    base_interval = 1.5 if "cnemc.cn" in domain else 0.8
    sleep_time = random.uniform(base_interval, base_interval + 2.0) # 1.5-3.5秒随机间隔
    time.sleep(sleep_time)

    max_attempts = max(1, int(getattr(__import__('config.settings'), 'MAX_RETRY_TIMES', MAX_RETRY_TIMES)))
    for attempt in range(1, max_attempts + 1):
        try:
            # 获取随机代理（每次重试可能更换代理）
            proxies = get_random_proxy() if USE_PROXY else None
            headers = get_headers(referer=referer or f'https://{domain}')
            response = session.get(
                url=url,
                params=params,
                headers=headers,
                proxies=proxies,
                timeout=timeout,
                verify=False  # 忽略SSL验证（部分网站可能证书过期）
            )
            response.raise_for_status()  # 触发HTTP错误
            response.encoding = response.apparent_encoding or "utf-8"
            logger.info(f" └─ ✅ 请求成功：{url}（状态码：{response.status_code}）")
            return response

        except requests.exceptions.HTTPError as e:
            logger.error(f" ├─ ❌ HTTP错误：{url}，状态码：{e.response.status_code if e.response else '未知'}，错误：{str(e)}")
            break
        except requests.exceptions.Timeout:
            logger.warning(f" ├─ ⏱️ 请求超时（第{attempt}次）：{url}（超时时间：{timeout}s）")
        except (ProtocolError, ConnectionResetError, socket.error) as e:
            # 底层连接被重置：尝试重建 session 并重试
            logger.warning(f" ├─ ！ 连接被重置（第{attempt}次）：{url}，错误：{repr(e)}")
            try:
                session.close()
            except Exception:
                pass
            # 重建 session，避免复用损坏的连接
            session = create_session()
        except requests.exceptions.RequestException as e:
            logger.error(f" ├─ ❌ 请求失败（第{attempt}次）：{url}，错误：{str(e)}")

        # 若需要重试，先等一段指数退避时间
        if attempt < max_attempts:
            backoff = (2 ** (attempt - 1)) + random.uniform(0, 1)
            logger.info(f"⏱️ 等待 {backoff:.1f}s 后重试（第{attempt + 1}次）: {url}")
            time.sleep(backoff)

    logger.error(f" └─ 🔄 多次重试失败：{url}")
    return None

def safe_post(session, url, params=None, data=None, timeout=15, referer=None, verify=False):
    """安全的POST请求：集成代理池、动态间隔、自动重试、添加伪装头并返回 response 或 None。
    
    与 safe_get 共享相同的重试逻辑和抗反爬策略，适用于需要POST方法的接口。
    """
    # 随机间隔优化（根据域名动态调整间隔）
    domain = url.split("//")[-1].split("/")[0]
    base_interval = 1.5 if "cnemc.cn" in domain else 0.8
    sleep_time = random.uniform(base_interval, base_interval + 2.0)  # 1.5-3.5秒随机间隔
    time.sleep(sleep_time)

    max_attempts = max(1, int(getattr(__import__('config.settings'), 'MAX_RETRY_TIMES', MAX_RETRY_TIMES)))
    for attempt in range(1, max_attempts + 1):
        try:
            # 获取随机代理（每次重试可能更换代理）
            proxies = get_random_proxy() if USE_PROXY else None
            headers = get_headers(referer=referer or f'https://{domain}')
            response = session.post(
                url=url,
                params=params,  # URL参数（?后的键值对）
                data=data,      # POST表单数据（body内容）
                headers=headers,
                proxies=proxies,
                timeout=timeout,
                verify=False  # 忽略SSL验证
            )
            response.raise_for_status()  # 触发HTTP错误
            response.encoding = response.apparent_encoding or "utf-8"
            logger.info(f" └─ ✅ POST请求成功：{url}（状态码：{response.status_code}）")
            return response

        except requests.exceptions.HTTPError as e:
            logger.error(f" ├─ ❌ POST HTTP错误：{url}，状态码：{e.response.status_code if e.response else '未知'}，错误：{str(e)}")
            break
        except requests.exceptions.Timeout:
            logger.warning(f" ├─ ⏱️ POST请求超时（第{attempt}次）：{url}（超时时间：{timeout}s）")
        except (ProtocolError, ConnectionResetError, socket.error) as e:
            # 底层连接被重置：重建session重试
            logger.warning(f" ├─ ！ POST连接被重置（第{attempt}次）：{url}，错误：{repr(e)}")
            try:
                session.close()
            except Exception:
                pass
            session = create_session()  # 重建会话
        except requests.exceptions.RequestException as e:
            logger.error(f" ├─ ❌ POST请求失败（第{attempt}次）：{url}，错误：{str(e)}")

        # 指数退避重试
        if attempt < max_attempts:
            backoff = (2 ** (attempt - 1)) + random.uniform(0, 1)
            logger.info(f"⏱️ 等待 {backoff:.1f}s 后重试（第{attempt + 1}次）: {url}")
            time.sleep(backoff)

    logger.error(f" └─ 🔄 POST多次重试失败：{url}")
    return None