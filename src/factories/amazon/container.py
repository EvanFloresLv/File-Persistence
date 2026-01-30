# ---------------------------------------------------------------------
# Internal application imports
# ---------------------------------------------------------------------
from src.application.use_cases import FileService

from src.infrastructure.amazon.s3 import S3Storage
from src.infrastructure.amazon.dynamodb import DynamoFileMetadataRepository
from src.infrastructure.amazon.clients import dynamo_client, s3_client


def file_service(
    bucket_name: str,
    folder: str,
    table_name: str
):
    """
    Create a FileService instance for Amazon S3 and DynamoDB.

    Args:
        bucket_name (str): The name of the S3 bucket.
        folder (str): The folder within the bucket.
        table_name (str): The DynamoDB table name.

    Returns:
        FileService: The configured FileService instance.
    """

    s3 = s3_client()
    dynamodb = dynamo_client()

    return FileService(
        repository=DynamoFileMetadataRepository(dynamodb, table_name),
        storage=S3Storage(s3, bucket_name, folder),
        folder=folder
    )
