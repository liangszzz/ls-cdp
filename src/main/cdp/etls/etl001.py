from awsglue.context import GlueContext

from src.main.cdp.common.base import Base
from src.main.cdp.common.config import Config, ConfigType
from src.main.cdp.common.options import ReadOptions, WriteOptions
from src.main.cdp.utils import glue_utils


class Etl(Base):
    def __init__(self, context: GlueContext, config: Config) -> None:
        super().__init__(context, config)

    def load_data(self) -> None:
        self.user_df = self.load_s3_file(
            "input1", ReadOptions.csv_options.value, format_map={"action_date": self.action_date}
        )
        self.address_df = self.load_s3_file(
            "input2", ReadOptions.csv_options.value, format_map={"action_date": self.action_date}
        )

    def handle_data(self) -> None:
        self.export_df = self.user_df.join(self.address_df, "address_code", "left").select("*")

    def export_data(self) -> None:
        self.export_to_s3(
            "output1", self.export_df, WriteOptions.csv_options.value, format_map={"action_date": self.action_date}
        )


if __name__ == "__main__":
    context = glue_utils.get_glue_context()
    config = Config(ConfigType.S3.value, "ryozen-glue", "etl002/etl002.ini", None)
    Etl(context, config).run()
