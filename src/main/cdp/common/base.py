import sys
from typing import Any, Dict, List, Union

from awsglue.context import DataFrame, GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions

from src.main.cdp.common import exceptions
from src.main.cdp.common.config import (
    Config,
    ConfigFile,
    InputOutputConfig,
    InputOutType,
)
from src.main.cdp.utils import glue_utils, s3_utils, sys_utils, time_utils
from src.main.cdp.utils.log_utils import get_logger
from src.main.cdp.utils.s3_utils import get_client


class Base:
    def __init__(self, context: GlueContext, config: Config) -> None:
        self.args: Dict[str, Any] = {}
        self.job: Job
        self.context = context
        self.spark = context.spark_session
        self.logger = get_logger(type(self).__name__)
        self.optional_params: List[str] = []
        self.require_params: List[str] = []
        self.config_dict: Dict[str, str] = {}
        self.config = config

    def init_config(self) -> None:
        self.config_dict = self.config.load_config()

    def logger_start(self) -> None:
        if ConfigFile.LOGGER_START_MSG.value in self.config_dict:
            self.logger.info(self.config_dict[ConfigFile.LOGGER_START_MSG.value])
        return None

    def init_optional_params(self) -> None:
        if ConfigFile.OPTIONAL_PARAMS.value in self.config_dict:
            arr = self.config_dict[ConfigFile.OPTIONAL_PARAMS.value].split(",")
            for item in arr:
                if sys_utils.check_sys_arg_exists(item, "--"):
                    self.optional_params.append(item)
        return None

    def init_required_params(self) -> None:
        if ConfigFile.REQUIRED_PARAMS.value in self.config_dict:
            self.require_params.extend(self.config_dict[ConfigFile.REQUIRED_PARAMS.value].split(","))
        return None

    def check_required_params(self) -> None:
        for param in self.require_params:
            if not sys_utils.check_sys_arg_exists(param, "--"):
                raise exceptions.ParamNotFoundException(param)

    def init_job(self) -> None:
        self.job = Job(self.context)
        self.optional_params.extend(self.require_params)

        self.args = getResolvedOptions(sys.argv, self.optional_params)
        self.job.init(self.args["JOB_NAME"], self.args)

    def handler_args(self) -> None:
        self.handler_action_date()
        return None

    def handler_action_date(self) -> None:
        if "action_date" in self.args:
            try:
                date_obj = time_utils.str_to_date(self.args["action_date"], time_utils.FORMAT_YYYYMMDD)
            except Exception as e:
                raise exceptions.DateFormatException(self.args["action_date"], time_utils.FORMAT_YYYYMMDD, e)
        else:
            date_obj = time_utils.get_today()
        self.action_date = time_utils.get_date_str(date_obj, time_utils.FORMAT_YYYYMMDD)

    def commit_job(self) -> None:
        self.job.commit()

    def load_data(self) -> None:
        return None

    def handle_data(self) -> None:
        return None

    def export_data(self) -> None:
        return None

    def logger_end(self) -> None:
        if ConfigFile.LOGGER_END_MSG.value in self.config_dict:
            self.logger.info(self.config_dict[ConfigFile.LOGGER_END_MSG.value])
        return None

    @exceptions.exception_decorator
    def run(self) -> None:
        self.init_config()
        self.logger_start()
        self.init_optional_params()
        self.init_required_params()
        self.check_required_params()
        self.init_job()
        self.handler_args()
        self.load_data()
        self.handle_data()
        self.export_data()
        self.commit_job()
        self.logger_end()

    def load_s3_file(
            self,
            section: str,
            optional_args: Dict[str, Any],
            cache_flag: bool = False,
            create_view_flag: bool = False,
            format_map: Union[None, Dict[str, str]] = None
    ) -> DataFrame:

        try:
            bucket = self.config_dict[f"{section}.{InputOutputConfig.BUCKET.value}"]
            prefix = self.config_dict[f"{section}.{InputOutputConfig.PATH.value}"]
            view_name = self.config_dict[f"{section}.{InputOutputConfig.TABLE_NAME.value}"]
            required = self.config_dict[f"{section}.{InputOutputConfig.REQUIRED.value}"]
            schema = self.config_dict[f"{section}.{InputOutputConfig.SCHEMA.value}"]
            file_type = self.config_dict[f"{section}.{InputOutputConfig.TYPE.value}"]

            success_msg = self.config_dict[f"{section}.{InputOutputConfig.SUCCESS_MSG.value}"]
            error_msg = self.config_dict[f"{section}.{InputOutputConfig.ERROR_MSG.value}"]
        except Exception as e:
            # TODO
            raise exceptions.BizException("BizException")

        if format_map is not None:
            bucket = bucket.format_map(format_map)
            prefix = prefix.format_map(format_map)
            view_name = view_name.format_map(format_map)
            required = required.format_map(format_map)
            schema = schema.format_map(format_map)
            file_type = file_type.format_map(format_map)
            success_msg = success_msg.format_map(format_map)
            error_msg = error_msg.format_map(format_map)

        s3 = get_client()

        s3_path = f"s3://{bucket}/{prefix}"
        if s3_utils.check_s3_file_or_dir_exist(s3, bucket, prefix, "dir" in file_type):
            if "csv" in file_type or "tsv" in file_type or "txt" in file_type or "fixed" in file_type:
                df = self.spark.read.csv(s3_path, **optional_args)
            elif "parquet" in file_type:
                df = self.spark.read.parquet(s3_path, **optional_args)
            else:
                raise exceptions.NotImplementedException()
        else:
            if required == "True":
                self.logger.error(error_msg.format_map({"bucket": bucket, "prefix": prefix}))
                raise exceptions.S3FileNotExistException(f"s3://{bucket}/{prefix}")
            else:
                df = self.context.createDataFrame([], schema)

        if glue_utils.check_df_count_is_zero(df):
            self.logger.warn("{} file's record number is 0".format(s3_path))

        if cache_flag:
            df.cache()

        if create_view_flag:
            df.createOrReplaceTempView(view_name)

        self.logger.info(success_msg)
        return df

    def export_to_s3(
            self,
            section: str,
            df: DataFrame,
            optional_args: Dict[str, Any],
            format_map: Union[None, Dict[str, str]] = None,
    ) -> None:

        file_type = self.config_dict[f"{section}.{InputOutputConfig.TYPE.value}"]
        bucket = self.config_dict[f"{section}.{InputOutputConfig.BUCKET.value}"]
        prefix = self.config_dict[f"{section}.{InputOutputConfig.PATH.value}"]
        success_msg = self.config_dict[f"{section}.{InputOutputConfig.SUCCESS_MSG.value}"]
        error_msg = self.config_dict[f"{section}.{InputOutputConfig.ERROR_MSG.value}"]

        if format_map is not None:
            bucket = bucket.format_map((format_map))
            prefix = prefix.format_map((format_map))
            file_type = file_type.format_map((format_map))
            success_msg = success_msg.format_map((format_map))
            error_msg = error_msg.format_map((format_map))

        try:
            if InputOutType.S3_DIR_PARQUET.value == file_type:
                df.write.mode("overwrite").parquet(f"s3://{bucket}/{prefix}", **optional_args)
            elif "csv" in file_type or "tsv" in file_type or "txt" in file_type:
                df.write.mode("overwrite").csv(f"s3://{bucket}/{prefix}", **optional_args)
            else:
                raise exceptions.NotImplementedException()
        except Exception as e:
            self.logger.error(error_msg)
            raise e

        self.logger.info(success_msg)
        return None
