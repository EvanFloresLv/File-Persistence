# ---------------------------------------------------------------------
# Third-party libraries
# ---------------------------------------------------------------------
from google.cloud.storage import Bucket
from google.api_core.exceptions import Forbidden

# ---------------------------------------------------------------------
# Internal application imports
# ---------------------------------------------------------------------
from src.domain.repositories import FileStorage


class GCSStorage(FileStorage):

    def __init__(
        self,
        bucket: Bucket
    ):
        self._bucket = bucket


    def upload(
        self,
        path: str,
        content: bytes,
        content_type: str
    ) -> None:
        blob = self._bucket.blob(path)
        blob.upload_from_string(content, content_type=content_type)
        print(f"Uploaded to {path} in bucket {self._bucket.name}")


    def delete(
        self,
        path: str
    ) -> None:
        prefix = path.rstrip("/") + "/"

        try:
            blobs = self._bucket.list_blobs(prefix=prefix)

            for blob in blobs:
                blob.delete()

        except Forbidden as exc:
            raise PermissionError(
                f"Missing permission to delete objects under: {prefix}"
            ) from exc