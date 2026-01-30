# ---------------------------------------------------------------------
# Third-party libraries
# ---------------------------------------------------------------------
import boto3


def dynamo_client():
    return boto3.client("dynamodb")


def s3_client():
    return boto3.client("s3")
