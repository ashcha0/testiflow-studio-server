import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config.constants import LOGS_DIR, LOG_LEVEL, LOG_FORMAT

# 获取项目根目录
project_root = Path(__file__).parent.parent.parent

def setup_logger(name: str, log_file: str = None) -> logging.Logger:
    """设置日志记录器
    
    Args:
        name: 日志记录器名称
        log_file: 日志文件名，如果为None则使用name作为文件名
        
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    logger = logging.getLogger(name)
    
    # 设置日志级别
    level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(level)
    
    # 创建格式化器
    formatter = logging.Formatter(LOG_FORMAT)
    
    # 添加控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 添加文件处理器
    if log_file is None:
        log_file = f"{name}.log"
    
    # 确保日志路径是基于项目根目录的绝对路径
    log_path = os.path.join(project_root, LOGS_DIR, log_file)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    file_handler = RotatingFileHandler(
        log_path, maxBytes=10*1024*1024, backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger