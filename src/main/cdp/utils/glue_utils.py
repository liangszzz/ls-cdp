import uuid
from typing import Any, Dict

from awsglue.context import DataFrame, GlueContext
from pyspark.context import SparkContext

from src.main.cdp.utils.s3_utils import get_client, rename_s3_file


def get_glue_context() -> GlueContext:
    return GlueContext(SparkContext())


def get_data_frame_from_catalog(context: GlueContext, database: str, table: str) -> DataFrame:
    """
    Creates a `DataFrame` from a Glue catalog database and table.

    Args:
        context (GlueContext): The Glue context object.
        database (str): The name of the database.
        table (str): The name of the table.

    Returns:
        DataFrame: The resulting `DataFrame`.
    """
    return context.create_data_frame.from_catalog(database, table)


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
    if "Contents" in response:
        for obj in response["Contents"]:
            if obj["Key"].startswith(f"{uuid_str}/part"):
                rename_s3_file(s3, bucket, bucket, obj["Key"], s3_path, True)


def check_df_count_is_zero(df: DataFrame) -> bool:
    """
    Checks if a DataFrame is empty
    :param df:
    :return:
    """
    return df.select("*").limit(1).count() == 0
