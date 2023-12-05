import os
import shutil
import sys

import pytest
from awsglue.context import GlueContext, SparkSession

from src.main.cdp.utils import log_utils
from src.main.cdp.utils.s3_utils import get_client

input_bucket = "cdp-input"
output_bucket = "cdp-output"

endpoint_url = "http://localstack:4566"
aws_access_key_id = "test"
region_name = "ap-northeast-1"

logger = log_utils.get_logger(__name__)

@pytest.fixture(scope="function", autouse=True)
def s3_handler():
    clear_sys_argv()
    s3=get_client()
    s3_delete_bucket(s3)
    s3_create_bucket(s3)

@pytest.fixture(scope="function")
def s3():
    return get_client()


@pytest.fixture(scope="function", autouse=False)
def local_pre():
    current_module_path = os.path.abspath(__file__)
    index = current_module_path.index("src/tests/cdp")
    current_module_path = current_module_path[:index]

    try:
        shutil.rmtree(f"{current_module_path}/download")
    except Exception as e:
        logger.error(e)
    return current_module_path



@pytest.fixture(scope="function")
def glue_context(tmpdir):
    spark_context = (
        SparkSession.builder.config("spark.hadoop.fs.s3a.endpoint", endpoint_url)
        .config("fs.s3a.access.key", aws_access_key_id)
        .config("fs.s3a.secret.key", aws_access_key_id)
        .config("spark.hadoop.fs.s3a.region", region_name)
        .config("spark.hadoop.fs.s3a.format", "json")
        .config("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("fs.s3a.path.style.access", "true")
        .config("fs.s3a.connection.ssl.enabled", "false")
        .config("com.amazonaws.services.s3a.enableV4", "true")
        .config("spark.driver.host", "localhost")
        .getOrCreate()
    )
    spark_context.sparkContext.setLogLevel("INFO")

    context = GlueContext(spark_context)
    yield (context)

    spark_context.stop()
    try:
        shutil.rmtree(tmpdir)
    except Exception as e:
        logger.error(e)


def s3_create_bucket(s3):
    logger.info("--------------------------start s3 bucket create---------------------------")
    for i in range(0, 10):
        try:
            s3.head_bucket(Bucket=input_bucket + str(i))
        except Exception:
            s3.create_bucket(
                Bucket=input_bucket + str(i),
                CreateBucketConfiguration={"LocationConstraint": region_name},
            )
    for i in range(0, 10):
        try:
            s3.head_bucket(Bucket=output_bucket + str(i))
        except Exception:
            s3.create_bucket(
                Bucket=output_bucket + str(i),
                CreateBucketConfiguration={"LocationConstraint": region_name},
            )
    logger.info("--------------------------end s3 bucket create---------------------------")


def s3_delete_bucket(s3):
    logger.info("--------------------------start s3 bucket delete---------------------------")
    for i in range(0, 10):
        delete_s3_bucket(input_bucket + str(i))

    for i in range(0, 10):
        delete_s3_bucket(output_bucket + str(i))

    logger.info("--------------------------end s3 bucket delete---------------------------")


def delete_s3_bucket(bucket: str):
    s3 = get_client()
    try:
        response = s3.list_objects_v2(Bucket=bucket)
        if "Contents" in response:
            objects = response["Contents"]
            for obj in objects:
                file_key = obj["Key"]
                s3.delete_object(Bucket=bucket, Key=file_key)
        s3.delete_bucket(Bucket=bucket)
    except Exception:
        logger.error("delete s3 bucket error")


def clear_sys_argv():
    logger.info("--------------------------start args init---------------------------")
    sys.argv.clear()
    sys.argv.append("--JOB_NAME")
    sys.argv.append("test")
    sys.argv.append("--JOB_NAME=test")
    sys.argv.append("--dev")
    logger.info("--------------------------end args init---------------------------")
