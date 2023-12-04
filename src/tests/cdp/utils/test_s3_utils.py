import sys

import pytest

from src.main.cdp.utils import s3_utils
from src.main.cdp.utils.s3_utils import upload_dir_or_file


def test_get_client():
    sys.argv.clear()
    s3_utils.s3_cache["s3"] = None
    client = s3_utils.get_client()
    assert client is not None


def test_get_client_2(s3):
    client = s3_utils.get_client()
    assert client == s3


def test_get_resource():
    sys.argv.clear()
    s3_utils.s3_cache["s3r"] = None
    resource = s3_utils.get_resource()
    assert resource is not None


def test_get_resource_2():
    resource = s3_utils.get_resource()
    resource2 = s3_utils.get_resource()
    assert resource == resource2


def test_check_s3_file_or_dir_exist(upload_data, s3):
    assert s3_utils.check_s3_file_or_dir_exist(s3, "cdp-input1", "a.csv", False)
    assert s3_utils.check_s3_file_or_dir_exist(s3, "cdp-input1", "b.csv", False) is False
    assert s3_utils.check_s3_file_or_dir_exist(s3, "cdp-input1", "a")
    assert s3_utils.check_s3_file_or_dir_exist(s3, "cdp-input1", "b") is False


def test_delete_s3_file(upload_data, s3):
    assert s3_utils.check_s3_file_or_dir_exist(s3, "cdp-input1", "a.csv", False)
    s3_utils.delete_s3_file(s3, "cdp-input1", "a.csv")
    assert s3_utils.check_s3_file_or_dir_exist(s3, "cdp-input1", "b.csv", False) is False


def test_read_s3_file(upload_data, s3):
    assert s3_utils.check_s3_file_or_dir_exist(s3, "cdp-input1", "a.csv", False)
    content = s3_utils.read_s3_file(s3, "cdp-input1", "a.csv")
    assert content == "aaaa"
    try:
        s3_utils.read_s3_file(s3, "cdp-input1", "b.csv")
    except Exception as e:
        assert e is not None


def test_rename_s3_file(upload_data, s3):
    assert s3_utils.check_s3_file_or_dir_exist(s3, "cdp-input1", "a.csv", False)
    s3_utils.rename_s3_file(s3, "cdp-input1", "cdp-input1", "a.csv", "b.csv", False)
    assert s3_utils.check_s3_file_or_dir_exist(s3, "cdp-input1", "a.csv", False)
    assert s3_utils.check_s3_file_or_dir_exist(s3, "cdp-input1", "b.csv", False)
    s3_utils.rename_s3_file(s3, "cdp-input1", "cdp-input1", "b.csv", "a.csv", True)
    assert s3_utils.check_s3_file_or_dir_exist(s3, "cdp-input1", "b.csv", False) is False


def test_download_s3_bucket(upload_data, s3, tmpdir):
    s3_utils.download_s3_bucket(s3, "cdp-input1", tmpdir)


@pytest.fixture(scope="function")
def upload_data(s3, local_pre):
    upload_dir_or_file(f"{local_pre}/src/tests/resources/utils/s3utils/input1", s3, "cdp-input1")
