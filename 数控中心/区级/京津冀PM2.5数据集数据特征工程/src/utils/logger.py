"""日志工具模块。

提供一个简易的文件日志初始化函数 `setup_logger`，按 `config/settings.py` 中配置的级别
与日志文件输出日志。项目中各模块通过 `from src.utils.logger import setup_logger` 获取日志实例。
"""

import logging
from config.settings import LOG_LEVEL, LOG_FILE


def setup_logger(name=__name__, log_file=None):
    level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    logger = logging.getLogger(name)
    if not logger.handlers:
        # 文件日志
        log_file_path = log_file if log_file else LOG_FILE
        fh = logging.FileHandler(log_file_path, encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        # 同时也添加控制台输出，方便在终端运行时观察日志
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        logger.addHandler(sh)
        # 防止日志消息向上传播到 root logger（避免控制台出现重复条目）
        logger.propagate = False
    logger.setLevel(level)
    return logger
