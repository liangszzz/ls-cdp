import pytest

from src.main.cdp.common.config import Config, ConfigType
from src.main.cdp.etls.demo.etl002 import Etl
from src.main.cdp.utils.s3_utils import download_s3_bucket, upload_dir_or_file


def test_run(glue_context, s3, caplog, tmpdir, local_pre, upload_data):
    config = Config(ConfigType.S3.value, "cdp-input0", "etl002.ini", None)
    etl = Etl(glue_context, config)
    etl.run()
    download_s3_bucket(s3, "cdp-output1", f"{local_pre}/download/cdp-output1")


@pytest.fixture(scope="function")
def upload_data(s3, local_pre):
    upload_dir_or_file(f"{local_pre}/src/tests/resources/etls/demo/etl002/config", s3, "cdp-input0")
    upload_dir_or_file(f"{local_pre}/src/tests/resources/etls/demo/etl002/input1", s3, "cdp-input1")
