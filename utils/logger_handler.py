"""日志工具模块"""
import logging
import os
from datetime import datetime
from utils.path_tool import get_project_root

def get_logger(name="zhisaotong", log_dir="logs", level=logging.INFO):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(level)

    log_folder = os.path.join(get_project_root(), log_dir)
    os.makedirs(log_folder, exist_ok=True)

    log_file = os.path.join(log_folder, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

logger = get_logger()
