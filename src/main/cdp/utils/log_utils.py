import datetime
import logging
import os
from logging.handlers import RotatingFileHandler

import pytz

from src.main.cdp.utils.sys_utils import is_dev_env


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    formatter.converter = lambda *args: datetime.datetime.now(pytz.timezone("Asia/Tokyo")).timetuple()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if is_dev_env():
        current_module_path = os.path.abspath(__file__)
        index = current_module_path.index("src/main/cdp")
        current_module_path = current_module_path[:index]

        file_handler = RotatingFileHandler(
            f"{current_module_path}/logger.log", encoding="utf-8", maxBytes=2 * 1024 * 1024, backupCount=1
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
