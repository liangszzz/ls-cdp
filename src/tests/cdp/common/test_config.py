import pytest

from src.main.cdp.common.config import Config, ConfigType
from src.main.cdp.utils.s3_utils import upload_dir_or_file


def test_load_config(upload_data):
    config = Config(ConfigType.S3.value, "cdp-code", "common.ini", None)
    config.load_config()

    config2 = Config(ConfigType.LOCAL.value, None, None, "src/tests/resources/common/config/config/common.ini")
    config2.load_config()

    config3 = Config("other", None, None, None)
    try:
        config3.load_config()
    except Exception as e:
        assert e is not None


@pytest.fixture(scope="function")
def upload_data(s3, local_pre):
    upload_dir_or_file(f"{local_pre}/src/tests/resources/common/config/config", s3, "cdp-code")
