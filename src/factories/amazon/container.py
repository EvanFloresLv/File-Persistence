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

    s3 = s3_client()
    dynamodb = dynamo_client()

    return FileService(
        repository=DynamoFileMetadataRepository(dynamodb, table_name),
        storage=S3Storage(s3, bucket_name, folder),
        folder=folder
    )
