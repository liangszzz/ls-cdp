from time import perf_counter
from typing import Any, Callable

from src.main.cdp.utils.log_utils import get_logger

logger = get_logger(__name__)


def time_decorator(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        start = perf_counter()
        res = func(*args, **kwargs)
        logger.info(f"{func.__name__} execute time: {perf_counter() - start}")
        return res

    return wrapper


def exception_decorator(func: Callable) -> Callable:
    @time_decorator
    def wrapper(*args, **kwargs) -> Any:
        try:
            logger.info(f"Start {func.__name__}")
            res = func(*args, **kwargs)
            logger.info(f"End {func.__name__}")
            return res
        except Exception as e:
            logger.error(e, exc_info=True)
            raise e

    return wrapper


class BizException(Exception):
    """
    business exception
    """

    def __init__(self, message, e=None):
        super().__init__(message)


class ParamNotFoundException(Exception):
    """
    parameter not found exception
    """

    def __init__(self, message, e=None):
        super().__init__("parameter [{0}] is not found".format(message))


class FileNotFoundException(Exception):
    """
    file not found exception
    """

    def __init__(self, message, e=None):
        super().__init__("file [{0}] is not found".format(message))


class S3FileNotExistException(Exception):
    """
    file not found exception
    """

    def __init__(self, s3_file_path, e=None):
        super().__init__("s3 file [{0}] is not found".format(s3_file_path))


class DateFormatException(Exception):
    """
    date format exception
    """

    def __init__(self, datestr, format, e=None):
        super().__init__("date [{0}] format is not [{1}]".format(datestr, format))


class NotImplementedException(Exception):
    """
    not implemented exception
    """

    def __init__(self, e=None):
        super().__init__("not implemented")
