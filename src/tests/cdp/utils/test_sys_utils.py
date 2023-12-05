from src.main.cdp.utils.sys_utils import check_sys_arg_exists, is_dev_env


def test_check_sys_arg_exists():
    assert check_sys_arg_exists("dev", "--")
    assert check_sys_arg_exists("aaa", "--") is False


def test_is_dev_env():
    assert is_dev_env()
