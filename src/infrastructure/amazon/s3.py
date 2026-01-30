# ---------------------------------------------------------------------
# Third-party libraries
# ---------------------------------------------------------------------
from types_boto3_s3.client import S3Client

# ---------------------------------------------------------------------
# Internal application imports
# ---------------------------------------------------------------------
from src.domain.repositories import FileStorage


class S3Storage(FileStorage):

    def __init__(
        self,
        bucket_name: str,
        s3_client: S3Client
    ):
        self._bucket = bucket_name
        self._client = s3_client


    def upload(
        self,
        path: str,
        content: bytes,
        content_type: str
    ) -> None:
        self._client.put_object(
            Bucket=self._bucket,
            Key=path,
            Body=content,
            ContentType=content_type
        )


    def delete(self, path: str) -> None:
        prefix = path.rstrip("/") + "/"
        paginator = self._client.get_paginator("list_objects_v2")

        batch = []

        for page in paginator.paginate(Bucket=self._bucket, Prefix=prefix):
            for obj in page.get("Contents", []):
                batch.append({"Key": obj["Key"]})

                if len(batch) == 1000:
                    self._delete_batch(batch)
                    batch.clear()

        if batch:
            self._delete_batch(batch)


    def _delete_batch(self, objects: list[dict]) -> None:
        response = self._client.delete_objects(
            Bucket=self._bucket,
            Delete={"Objects": objects}
        )

        errors = response.get("Errors", [])
        if errors:
            raise RuntimeError(
                f"Failed to delete {len(errors)} objects from S3: {errors}"
            )
