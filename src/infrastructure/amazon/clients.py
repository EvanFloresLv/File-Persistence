# ---------------------------------------------------------------------
# Third-party libraries
# ---------------------------------------------------------------------
import boto3


def dynamo_client():
    """
    Create a DynamoDB client.
    """
    return boto3.client("dynamodb")


def s3_client():
    """
    Create an S3 client.
    """
    return boto3.client("s3")
