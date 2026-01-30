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
    """
    Google Cloud Storage implementation of FileStorage.
    """

    def __init__(
        self,
        bucket: Bucket
    ):
        """
        Initialize the GCSStorage with a Google Cloud Storage bucket.

        Args:
            bucket (Bucket): The Google Cloud Storage bucket to use.

        Returns:
            None
        """
        self._bucket = bucket


    def upload(
        self,
        path: str,
        content: bytes,
        content_type: str
    ) -> None:
        """
        Upload a file to Google Cloud Storage.

        Args:
            path (str): The path to the file in Google Cloud Storage.
            content (bytes): The content of the file to upload.
            content_type (str): The MIME type of the file.

        Returns:
            None
        """

        blob = self._bucket.blob(path)
        blob.upload_from_string(content, content_type=content_type)
        print(f"Uploaded to {path} in bucket {self._bucket.name}")


    def delete(
        self,
        path: str
    ) -> None:
        """
        Delete a file from Google Cloud Storage.

        Args:
            path (str): The path to the file in Google Cloud Storage.

        Returns:
            None
        """

        prefix = path.rstrip("/") + "/"
        print(f"Deleting all blobs under prefix: {prefix}")

        try:
            blobs = list(self._bucket.list_blobs(prefix=prefix))

            if not blobs:
                print(f"No blobs found under prefix: {prefix}")

            for blob in blobs:
                blob.delete()
                print(f"Deleted {blob.name} from bucket {self._bucket.name}")

        except Forbidden as exc:
            raise PermissionError(
                f"Missing permission to delete objects under: {prefix}"
            ) from exc