# ---------------------------------------------------------------------
# Internal application imports
# ---------------------------------------------------------------------
from src.services.files import FileService

from src.providers.google.gcs import GCSStorage
from src.providers.google.firestore import FirestoreFileMetadataRepository
from src.providers.google.clients import firestore_client, gcs_client


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
