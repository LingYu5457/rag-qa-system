import logging
import sys
from datetime import datetime
from pathlib import Path

def setup_logger(name: str = "RAG_System", log_dir: str = "logs") -> logging.Logger:
    """
    配置统一的日志系统
    
    Args:
        name: 日志记录器名称
        log_dir: 日志文件目录
    
    Returns:
        配置好的logger
    """
    # 创建日志目录
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    # 创建logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # 设置最低级别
    
    # 避免重复添加handler
    if logger.handlers:
        return logger
    
    # 日志格式
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 控制台输出 - INFO级别以上
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件输出 - DEBUG级别（所有日志）
    log_file = Path(log_dir) / f"rag_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # 错误文件单独输出
    error_file = Path(log_dir) / f"error_{datetime.now().strftime('%Y%m%d')}.log"
    error_handler = logging.FileHandler(error_file, encoding='utf-8')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)
    
    return logger