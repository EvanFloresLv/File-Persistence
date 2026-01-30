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

    fs = firestore_client()
    gcs = gcs_client()

    bucket = gcs.bucket(bucket_name)
    collection = fs.collection(collection_name)

    return FileService(
        repository=FirestoreFileMetadataRepository(collection),
        storage=GCSStorage(bucket),
        folder=folder
    )
