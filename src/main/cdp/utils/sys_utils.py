import configparser
import sys
from typing import Dict


def check_sys_arg_exists(arg: str, prefix: str) -> bool:
    """
    Check if the given argument exists.

    Args:
        arg (str): the argument to check.
        prefix (str): the prefix of the argument.
    Returns:
        bool: True if the argument exists, False otherwise.
    """
    for param in sys.argv:
        if param.startswith(f"{prefix}{arg}"):
            return True
    return False


def read_config_to_json(path: str) -> Dict[str, Dict[str, str]]:
    """
    Read a config file and convert it to a dictionary.
    :param path:
    :return:
    """
    config = configparser.ConfigParser()
    config.read(path)
    config_dict: Dict[str, Dict[str, str]] = {}
    for section in config.sections():
        config_dict[section] = {}
        for option in config.options(section):
            config_dict[section][option] = config.get(section, option)
    return config_dict


def is_dev_env() -> bool:
    """
    Check if the current environment is dev.
    """
    return check_sys_arg_exists("dev", "--")
