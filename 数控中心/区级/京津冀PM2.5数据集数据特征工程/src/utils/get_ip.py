"""IP查询工具模块"""
import requests
import re
from config.settings import TUNNEL_PROXY, USE_TUNNEL_PROXY  # 引入代理配置

def get_current_ip():
    """
    获取当前公网IP（支持隧道代理环境）
    返回值: 字符串格式的IP地址或错误信息
    """
    # 备选API列表
    apis = [
        "https://api.ipify.org?format=json",  # 原API
        "https://icanhazip.com",             # 返回纯文本IP
        "https://ipinfo.io/ip",              # 返回纯文本IP
        "https://ifconfig.me/ip",            # 返回纯文本IP
        "https://ip.cn/ip",                  # 国内服务，返回IP+地区
    ]
    for api in apis:
        try:
            # 构建代理配置（如果启用隧道代理）
            proxies = None
            if USE_TUNNEL_PROXY and TUNNEL_PROXY:
                tunnel = TUNNEL_PROXY["tunnel"]
                username = TUNNEL_PROXY["username"]
                password = TUNNEL_PROXY["password"]
                proxies = {
                    "http": f"http://{username}:{password}@{tunnel}",
                    "https": f"https://{username}:{password}@{tunnel}"  # 补充HTTPS代理
                }
            
            # 调用IP查询接口（无论是否启用代理，统一在此处发起请求）
            response = requests.get(
                api,
                proxies=proxies,
                timeout=5,
                verify=False  # 与项目保持一致的SSL策略
            )
            response.raise_for_status()  # 触发HTTP错误
            
            # 处理不同API的返回格式
            if api.endswith("json"):
                ip = response.json().get("ip")
                if ip:
                    return ip
            else:
                # 提取纯文本IP（处理ip.cn的特殊格式）
                text = response.text.strip()
                ip_match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text)
                if ip_match:
                    return ip_match.group()
        
        except Exception as e:
            # 单个API失败，继续尝试下一个
            continue
    
    # 所有API都失败时返回错误
    return "获取IP失败：所有备选接口均无法访问"