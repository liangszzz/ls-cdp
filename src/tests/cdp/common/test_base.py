import sys

import pytest

from src.main.cdp.common.base import Base
from src.main.cdp.common.config import Config, ConfigFile, ConfigType, InputOutputConfig
from src.main.cdp.utils.s3_utils import upload_dir_or_file


def test_logger_start_end(glue_context, upload_data, caplog):
    sys.argv.append("--action_date=20231020")
    config = Config(ConfigType.S3, "cdp-input0", "common.ini", None)
    etl = Base(glue_context, config)
    etl.init_config()
    etl.logger_start()
    assert caplog.records[0].message == "Start ETL001_CSV ETL"
    assert caplog.records[0].levelname == "INFO"

    del etl.config_dict[ConfigFile.LOGGER_START_MSG.value]
    etl.logger_start()
    assert len(caplog.records) == 1

    etl.logger_end()

    assert caplog.records[1].message == "End ETL001_CSV ETL"
    assert caplog.records[1].levelname == "INFO"

    del etl.config_dict[ConfigFile.LOGGER_END_MSG.value]

    etl.logger_end()

    assert len(caplog.records) == 2


def test_init_optional_params_1(glue_context, upload_data):
    config = Config(ConfigType.S3, "cdp-input0", "common.ini", None)
    etl = Base(glue_context, config)
    etl.init_config()
    etl.init_optional_params()


def test_init_optional_params_2(glue_context, upload_data):
    config = Config(ConfigType.S3, "cdp-input0", "common.ini", None)
    etl = Base(glue_context, config)
    etl.init_config()
    etl.config_dict[ConfigFile.OPTIONAL_PARAMS.value] = "action_date"
    etl.init_optional_params()


def test_init_optional_params_3(glue_context, upload_data):
    sys.argv.append("--action_date=20231020")
    config = Config(ConfigType.S3, "cdp-input0", "common.ini", None)
    etl = Base(glue_context, config)
    etl.init_config()
    etl.config_dict[ConfigFile.OPTIONAL_PARAMS.value] = "action_date"
    etl.init_optional_params()


def test_init_optional_params_4(glue_context, upload_data):
    sys.argv.append("--action_date=20231020")
    config = Config(ConfigType.S3, "cdp-input0", "common.ini", None)
    etl = Base(glue_context, config)
    etl.init_config()
    del etl.config_dict[ConfigFile.OPTIONAL_PARAMS.value]
    etl.init_optional_params()


def test_init_required_params_1(glue_context, upload_data):
    config = Config(ConfigType.S3, "cdp-input0", "common.ini", None)
    etl = Base(glue_context, config)
    etl.init_config()
    etl.init_required_params()


def test_init_required_params_2(glue_context, upload_data):
    config = Config(ConfigType.S3, "cdp-input0", "common.ini", None)
    etl = Base(glue_context, config)
    etl.init_config()
    del etl.config_dict[ConfigFile.REQUIRED_PARAMS.value]
    etl.init_required_params()


def test_init_required_params_3(glue_context, upload_data):
    config = Config(ConfigType.S3, "cdp-input0", "common.ini", None)
    etl = Base(glue_context, config)
    etl.init_config()
    etl.config_dict[ConfigFile.REQUIRED_PARAMS.value] = ""
    etl.init_required_params()


def test_check_required_params_1(glue_context, upload_data):
    config = Config(ConfigType.S3, "cdp-input0", "common.ini", None)
    etl = Base(glue_context, config)
    etl.init_config()
    etl.init_required_params()
    etl.check_required_params()


def test_check_required_params_2(glue_context, upload_data):
    config = Config(ConfigType.S3, "cdp-input0", "common.ini", None)
    etl = Base(glue_context, config)
    etl.init_config()

    etl.config_dict[ConfigFile.REQUIRED_PARAMS.value] = "JOB_NAME,MY_PARAM"
    etl.init_required_params()
    try:
        etl.check_required_params()
    except Exception as e:
        assert e is not None


def test_run(glue_context, upload_data):
    config = Config(ConfigType.S3, "cdp-input0", "common.ini", None)
    etl = Base(glue_context, config)
    etl.run()


def test_handler_action_date_1(glue_context, upload_data):
    sys.argv.append("--action_date=20231020")
    config = Config(ConfigType.S3, "cdp-input0", "common.ini", None)
    etl = Base(glue_context, config)
    etl.init_config()
    etl.config_dict[ConfigFile.OPTIONAL_PARAMS.value] = "action_date"
    etl.init_optional_params()
    etl.init_required_params()

    etl.init_job()
    etl.handler_action_date()


def test_handler_action_date_2(glue_context, upload_data):
    sys.argv.append("--action_date=20231020XXX")
    config = Config(ConfigType.S3, "cdp-input0", "common.ini", None)
    etl = Base(glue_context, config)
    etl.init_config()
    etl.config_dict[ConfigFile.OPTIONAL_PARAMS.value] = "action_date"
    etl.init_optional_params()
    etl.init_required_params()

    etl.init_job()
    try:
        etl.handler_action_date()
    except Exception as e:
        assert e is not None


def test_load_s3_file_1(glue_context, upload_data):
    config = Config(ConfigType.S3, "cdp-input0", "common.ini", None)
    etl = Base(glue_context, config)
    etl.init_config()
    del etl.config_dict["input1.bucket"]
    try:
        etl.load_s3_file(
            "input1",
            optional_args={},
            format_map={
                "input_file_type": "",
                "input_file_bucket": "cdp-input1",
                "input_file_path": "",
                "output_file_type": "",
                "output_file_bucket": "",
                "output_file_path": "",
            },
        )
    except Exception as e:
        assert e is not None


def test_load_s3_file_2(glue_context, upload_data):
    config = Config(ConfigType.S3, "cdp-input0", "common.ini", None)
    etl = Base(glue_context, config)
    etl.init_config()

    try:
        etl.load_s3_file("input1", optional_args={})
    except Exception as e:
        assert e is not None

    df = etl.load_s3_file(
        "input1",
        optional_args={},
        format_map={
            "input_file_type": "s3-dir-csv",
            "input_file_bucket": "cdp-input1",
            "input_file_path": "path/001/20231020/user.csv",
        },
    )
    assert df is not None

    df = etl.load_s3_file(
        "input1",
        optional_args={},
        format_map={
            "input_file_type": "s3-dir-tsv",
            "input_file_bucket": "cdp-input1",
            "input_file_path": "path/001/20231020/user.csv",
        },
    )
    assert df is not None

    df = etl.load_s3_file(
        "input1",
        optional_args={},
        cache_flag=True,
        format_map={
            "input_file_type": "s3-dir-txt",
            "input_file_bucket": "cdp-input1",
            "input_file_path": "path/001/20231020/user.txt",
        },
    )
    assert df is not None

    df = etl.load_s3_file(
        "input1",
        optional_args={},
        create_view_flag=True,
        format_map={
            "input_file_type": "s3-dir-fixed",
            "input_file_bucket": "cdp-input1",
            "input_file_path": "path/001/20231020/user.csv",
        },
    )
    assert df is not None

    df = etl.load_s3_file(
        "input1",
        optional_args={},
        format_map={
            "input_file_type": "s3-dir-parquet",
            "input_file_bucket": "cdp-input1",
            "input_file_path": "path/001/20231020/user.parquet",
        },
    )
    assert df is not None

    try:
        etl.load_s3_file(
            "input1",
            optional_args={},
            format_map={
                "input_file_type": "avv",
                "input_file_bucket": "cdp-input1",
                "input_file_path": "path/001/20231020/A.a",
            },
        )
    except Exception as e:
        assert e is not None

    try:
        etl.config_dict[f"input1.{InputOutputConfig.REQUIRED.value}"] = "False"
        etl.load_s3_file(
            "input1",
            optional_args={},
            format_map={
                "input_file_type": "s3-dir-fixed",
                "input_file_bucket": "cdp-input1",
                "input_file_path": "path/001/20231020/A.a",
            },
        )
    except Exception as e:
        assert e is not None

    try:
        etl.load_s3_file(
            "input1",
            optional_args={},
            format_map={
                "input_file_type": "avv",
                "input_file_bucket": "cdp-input1",
                "input_file_path": "path/001/20231020/user.parquet",
            },
        )
    except Exception as e:
        assert e is not None


def test_export_tos3_1(glue_context, upload_data):
    config = Config(ConfigType.S3, "cdp-input0", "common.ini", None)
    etl = Base(glue_context, config)
    etl.init_config()
    del etl.config_dict["output1.bucket"]
    df = etl.load_s3_file(
        "input1",
        optional_args={},
        format_map={
            "input_file_type": "s3-dir-csv",
            "input_file_bucket": "cdp-input1",
            "input_file_path": "path/001/20231020/user.csv",
        },
    )
    assert df is not None

    try:
        etl.export_to_s3("output1", df, optional_args={})
    except Exception as e:
        assert e is not None


def test_export_tos3_2(glue_context, upload_data):
    config = Config(ConfigType.S3, "cdp-input0", "common.ini", None)
    etl = Base(glue_context, config)
    etl.init_config()
    df = etl.load_s3_file(
        "input1",
        optional_args={},
        format_map={
            "input_file_type": "s3-dir-csv",
            "input_file_bucket": "cdp-input1",
            "input_file_path": "path/001/20231020/user.csv",
        },
    )
    assert df is not None

    try:
        etl.export_to_s3(
            "output1",
            df,
            optional_args={},
        )
    except Exception as e:
        assert e is not None

    etl.export_to_s3(
        "output1",
        df,
        optional_args={},
        format_map={
            "output_file_type": "s3-dir-parquet",
            "output_file_bucket": "cdp-output1",
            "output_file_path": "path/parquet",
        },
    )

    etl.export_to_s3(
        "output1",
        df,
        optional_args={},
        format_map={
            "output_file_type": "s3-dir-csv",
            "output_file_bucket": "cdp-output1",
            "output_file_path": "path/csv",
        },
    )

    etl.export_to_s3(
        "output1",
        df,
        optional_args={},
        format_map={
            "output_file_type": "s3-dir-tsv",
            "output_file_bucket": "cdp-output1",
            "output_file_path": "path/tsv",
        },
    )

    etl.export_to_s3(
        "output1",
        df,
        optional_args={},
        format_map={
            "output_file_type": "s3-dir-txt",
            "output_file_bucket": "cdp-output1",
            "output_file_path": "path/tsv",
        },
    )

    try:
        etl.export_to_s3(
            "output1",
            df,
            optional_args={},
            format_map={
                "output_file_type": "abc",
                "output_file_bucket": "cdp-output1",
                "output_file_path": "path/tsv",
            },
        )
    except Exception as e:
        assert e is not None


@pytest.fixture(scope="function")
def upload_data(s3, local_pre):
    upload_dir_or_file(f"{local_pre}/src/tests/resources/common/base/config", s3, "cdp-input0")
    upload_dir_or_file(f"{local_pre}/src/tests/resources/common/base/input1", s3, "cdp-input1")
