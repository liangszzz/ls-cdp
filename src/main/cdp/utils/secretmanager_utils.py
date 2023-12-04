from typing import Union

from boto3 import client

from src.main.cdp.common.exceptions import BizException


def get_value(secret_name: str, region_name: str = "ap-northeast-1", endpoint_url: Union[str, None] = None) -> str:
    if endpoint_url is None:
        secretsmanager = client("secretsmanager", region_name=region_name)
    else:
        secretsmanager = client("secretsmanager", region_name=region_name, endpoint_url=endpoint_url)

    response = secretsmanager.get_secret_value(SecretId=secret_name)
    if "SecretString" in response:
        return response["SecretString"]

    raise BizException("Secret not found", None)


def create_value(
    secret_name: str, secret_value: str, region_name: str = "ap-northeast-1", endpoint_url: Union[str, None] = None
) -> None:
    if endpoint_url is None:
        secretsmanager = client("secretsmanager", region_name=region_name)
    else:
        secretsmanager = client("secretsmanager", region_name=region_name, endpoint_url=endpoint_url)

    response = secretsmanager.create_secret(
        SecretId=secret_name,
        SecretString=secret_value,
    )
    if "Name" not in response:
        raise BizException("Secret create error", None)
