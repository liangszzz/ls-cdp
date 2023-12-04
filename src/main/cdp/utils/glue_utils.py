import uuid
from typing import Any, Dict

from awsglue.context import DataFrame, GlueContext
from pyspark.context import SparkContext

from src.main.cdp.utils.s3_utils import get_client, rename_s3_file


def get_glue_context() -> GlueContext:
    return GlueContext(SparkContext())


def export_df_to_csv_file(df: DataFrame, bucket: str, s3_path: str, options: Dict[str, Any]) -> None:
    """
    Exports a specified DataFrame, `df`, to a CSV file stored on S3
    :param df:
    :param bucket:
    :param s3_path:
    :param options:
    :return:
    """
    df = df.repartition(1)
    uuid_str = str(uuid.uuid4())
    s3_tmp_path = f"s3://{bucket}/{uuid_str}"
    s3 = get_client()
    df.write.mode("overwrite").csv(s3_tmp_path, **options)
    response = s3.list_objects(Bucket=bucket, Prefix=f"{uuid_str}")
    for obj in response["Contents"]:
        rename_s3_file(s3, bucket, bucket, obj["Key"], s3_path, True)


def check_df_count_is_zero(df: DataFrame) -> bool:
    """
    Checks if a DataFrame is empty
    :param df:
    :return:
    """
    return df.select("*").limit(1).count() == 0
