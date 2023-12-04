import sys

import pytest

from src.main.cdp.common.config import Config, ConfigType
from src.main.cdp.etls.demo.etl001 import Etl
from src.main.cdp.utils.s3_utils import download_s3_bucket, upload_dir_or_file


def test_run_csv(glue_context, s3, caplog, tmpdir, local_pre, upload_data):
    sys.argv.append("--action_date=20231020")
    sys.argv.append("--input_file_type=s3-dir-csv")
    sys.argv.append("--input_file_bucket=cdp-input1")
    sys.argv.append("--input_file_path=path/001")
    sys.argv.append("--output_file_bucket=cdp-output1")
    sys.argv.append("--output_file_path=path/001")
    sys.argv.append("--decimal_columns=age")
    sys.argv.append("--date_columns=birthday")
    sys.argv.append("--date_fromat=yyyy-MM-dd")

    config = Config(ConfigType.S3.value, "cdp-input0", "etl001.ini", None)
    etl = Etl(glue_context, config)
    etl.run()
    download_s3_bucket(s3, "cdp-output1", f"{local_pre}/download/cdp-output1")


def test_run_tsv(glue_context, s3, caplog, tmpdir, local_pre, upload_data):
    sys.argv.append("--action_date=20231020")
    sys.argv.append("--input_file_type=s3-dir-tsv")
    sys.argv.append("--input_file_bucket=cdp-input1")
    sys.argv.append("--input_file_path=path/002")
    sys.argv.append("--output_file_bucket=cdp-output1")
    sys.argv.append("--output_file_path=path/002")
    sys.argv.append("--decimal_columns=age")
    sys.argv.append("--date_columns=birthday")
    sys.argv.append("--date_fromat=yyyy-MM-dd")

    config = Config(ConfigType.S3.value, "cdp-input0", "etl001.ini", None)
    etl = Etl(glue_context, config)
    etl.run()
    download_s3_bucket(s3, "cdp-output1", f"{local_pre}/download/cdp-output1")


def test_run_txt(glue_context, s3, caplog, tmpdir, local_pre, upload_data):
    sys.argv.append("--action_date=20231020")
    sys.argv.append("--input_file_type=s3-dir-txt")
    sys.argv.append("--input_file_bucket=cdp-input1")
    sys.argv.append("--input_file_path=path/003")
    sys.argv.append("--output_file_bucket=cdp-output1")
    sys.argv.append("--output_file_path=path/003")
    sys.argv.append("--decimal_columns=age")
    sys.argv.append("--date_columns=birthday")
    sys.argv.append("--date_fromat=yyyy-MM-dd")

    config = Config(ConfigType.S3.value, "cdp-input0", "etl001.ini", None)
    etl = Etl(glue_context, config)
    etl.run()
    download_s3_bucket(s3, "cdp-output1", f"{local_pre}/download/cdp-output1")


def test_run_abc(glue_context, s3, caplog, tmpdir, local_pre, upload_data):
    sys.argv.append("--action_date=20231020")
    sys.argv.append("--input_file_type=s3-dir-abc")
    sys.argv.append("--input_file_bucket=cdp-input1")
    sys.argv.append("--input_file_path=path/003")
    sys.argv.append("--output_file_bucket=cdp-output1")
    sys.argv.append("--output_file_path=path/003")
    sys.argv.append("--decimal_columns=age")
    sys.argv.append("--date_columns=birthday")
    sys.argv.append("--date_fromat=yyyy-MM-dd")

    config = Config(ConfigType.S3.value, "cdp-input0", "etl001.ini", None)
    etl = Etl(glue_context, config)
    try:
        etl.run()
    except Exception as e:
        assert e is not None


@pytest.fixture(scope="function")
def upload_data(s3, local_pre):
    upload_dir_or_file(f"{local_pre}/src/tests/resources/etls/demo/etl001/config", s3, "cdp-input0")
    upload_dir_or_file(f"{local_pre}/src/tests/resources/etls/demo/etl001/input1", s3, "cdp-input1")
