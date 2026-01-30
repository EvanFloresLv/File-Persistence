# ---------------------------------------------------------------------
# Internal application imports
# ---------------------------------------------------------------------
from src.application.use_cases import FileService

from src.infrastructure.google.gcs import GCSStorage
from src.infrastructure.google.firestore import FirestoreFileMetadataRepository
from src.infrastructure.google.clients import firestore_client, gcs_client


def file_service(
    bucket_name: str,
    folder: str,
    collection_name: str
):
    """
    Create a FileService instance for Google Cloud Storage and Firestore.

    Args:
        bucket_name (str): The name of the GCS bucket.
        folder (str): The folder within the bucket.
        collection_name (str): The Firestore collection name.

    Returns:
        FileService: The configured FileService instance.
    """

    fs = firestore_client()
    gcs = gcs_client()

    bucket = gcs.bucket(bucket_name)
    collection = fs.collection(collection_name)

    return FileService(
        repository=FirestoreFileMetadataRepository(collection),
        storage=GCSStorage(bucket),
        folder=folder
    )
