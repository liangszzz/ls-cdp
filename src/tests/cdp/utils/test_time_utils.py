from src.main.cdp.utils.time_utils import *


def test_get_today():
    assert get_today() is not None


def test_get_yesterday():
    assert get_yesterday() is not None


def test_get_now():
    assert get_now() is not None


def test_get_time_str():
    assert get_time_str() is not None


def test_get_date_str():
    assert get_date_str(get_now()) is not None


def test_str_to_date():
    assert str_to_date("2020-01-01") is not None


def test_str_to_datetime():
    assert str_to_datetime("2020-01-01 10:10:10") is not None
