from awsglue.context import GlueContext
from pyspark.sql.functions import col, regexp_replace, to_date, trim

from src.main.cdp.common.base import Base
from src.main.cdp.common.config import Config, ConfigType
from src.main.cdp.common.exceptions import NotImplementedException
from src.main.cdp.common.options import ReadOptions, WriteOptions
from src.main.cdp.utils import glue_utils


class Etl(Base):
    def __init__(self, context: GlueContext, config: Config) -> None:
        super().__init__(context, config)

    def handler_args(self) -> None:
        super().handler_args()

    def load_data(self) -> None:
        if "csv" in self.args["input_file_type"] or "txt" in self.args["input_file_type"]:
            optional_args = ReadOptions.csv_options.value
        elif "tsv" in self.args["input_file_type"]:
            optional_args = ReadOptions.tsv_options.value
        else:
            raise NotImplementedException()

        self.input_df = self.load_s3_file(
            "input1",
            optional_args,
            create_view_flag=False,
            format_map={
                "action_date": self.action_date,
                "input_file_type": self.args["input_file_type"],
                "input_file_bucket": self.args["input_file_bucket"],
                "input_file_path": self.args["input_file_path"],
            },
        )

    def handle_data(self) -> None:
        decimal_columns = self.args["decimal_columns"].split(",")
        date_columns = self.args["date_columns"].split(",")

        columns = self.input_df.columns
        df = self.input_df

        for column in columns:
            # a.trim
            df = df.withColumn(column, trim(col(column)))
            # b.decimal parse
            if column in decimal_columns:
                df = df.withColumn(column, regexp_replace(column, "\\.$", "")).withColumn(
                    column, col(column).cast("decimal(15,2)")
                )
            # c.date parse
            if column in date_columns:
                df = df.withColumn(column, regexp_replace(column, "\\.$", "")).withColumn(
                    column, to_date(col(column), self.args["date_fromat"])
                )

        self.export_df = df

    def export_data(self) -> None:
        self.export_df.show()
        self.export_to_s3(
            "output1",
            self.export_df,
            WriteOptions.parquet_options.value,
            format_map={
                "action_date": self.action_date,
                "output_file_bucket": self.args["output_file_bucket"],
                "output_file_path": self.args["output_file_path"],
            },
        )


if __name__ == "__main__":
    context = glue_utils.get_glue_context()
    config = Config(ConfigType.S3.value, "ryozen-glue", "etl001/etl001.ini", None)
    Etl(context, config).run()
