import uuid

import pytest
from boto3 import client

from src.main.cdp.utils.secretmanager_utils import create_value, get_value


def test_create_key(del_secret_key):
    secret_id = str(uuid.uuid4()).replace("-", "")
    try:
        create_value(secret_id, "cdp")
    except Exception as e:
        assert e is not None


def test_run_success(del_secret_key):
    secret_id = str(uuid.uuid4()).replace("-", "")
    create_value(secret_id, "cdp", endpoint_url="http://localstack:4566")
    response = get_value(secret_id, endpoint_url="http://localstack:4566")
    assert response == "cdp"


def test_run_fail(del_secret_key):
    secret_id = str(uuid.uuid4()).replace("-", "")
    create_value(secret_id, "cdp", endpoint_url="http://localstack:4566")
    try:
        get_value(secret_id)
    except Exception as e:
        assert e is not None

    try:
        get_value(secret_id + "a", endpoint_url="http://localstack:4566")
    except Exception as e:
        print(e)
        assert e is not None


@pytest.fixture()
def del_secret_key():
    secretsmanager = client("secretsmanager", region_name="ap-northeast-1", endpoint_url="http://localstack:4566")
    paginator = secretsmanager.get_paginator("list_secrets")
    for page in paginator.paginate():
        for secret in page["SecretList"]:
            if "DeletedDate" in secret and secret["DeletedDate"] is not None:
                pass
            else:
                secretsmanager.delete_secret(SecretId=secret["Name"])
