# ---------------------------------------------------------------------
# Standard library
# ---------------------------------------------------------------------
from typing import List, Optional, Type, TypeVar
from dataclasses import asdict

# ---------------------------------------------------------------------
# Third-party library imports
# ---------------------------------------------------------------------
from boto3.dynamodb.conditions import Key, Attr

# ---------------------------------------------------------------------
# Internal application imports
# ---------------------------------------------------------------------
from src.domain.repositories import FileMetadataRepository


TVersion = TypeVar("TVersion")


class DynamoFileMetadataRepository(FileMetadataRepository):
    """
    DynamoDB implementation of the FileMetadataRepository interface.
    """

    def __init__(
        self,
        table,
        version_cls: Type[TVersion]
    ):
        """
        Initialize the DynamoFileMetadataRepository with a DynamoDB table and a version class.

        Args:
            table: The DynamoDB table to use.
            version_cls (Type[TVersion]): The version class to use for deserialization.

        Returns:
            None
        """

        self._table = table
        self._version_cls = version_cls


    def get_active(
        self,
        id: str
    ) -> Optional[TVersion]:
        """
        Get the active version of a file by its ID.

        Args:
            id (str): The ID of the file to retrieve.

        Returns:
            Optional[TVersion]: The active version of the file, or None if not found.
        """

        response = self._table.query(
            KeyConditionExpression=Key("id").eq(id),
            FilterExpression=Attr("status").eq("ACTIVE"),
            Limit=1,
            ScanIndexForward=False
        )

        items = response.get("Items", [])

        if not items:
            return None

        return self._deserialize(items[0])


    def get_versions(
        self,
        id: str
    ) -> List[TVersion]:
        """
        Get all versions of a file by its ID.

        Args:
            id (str): The ID of the file to retrieve.

        Returns:
            List[TVersion]: A list of all versions of the file.
        """

        response = self._table.query(
            KeyConditionExpression=Key("id").eq(id),
            ScanIndexForward=False
        )

        items = response.get("Items", [])
        return [self._deserialize(item) for item in items]


    def deactivate_versions(
        self,
        id: str
    ) -> None:
        """
        Deactivate all versions of a file by its ID.

        Args:
            id (str): The ID of the file to deactivate.

        Returns:
            None
        """

        active = self.get_active(id)

        if not active:
            return

        self._table.update_item(
            Key={"id": id},
            UpdateExpression="SET #status = :inactive",
            ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues={":inactive": "INACTIVE"}
        )

    def delete_versions(
        self,
        id: str
    ) -> None:
        """
        Delete all versions of a file by its ID.

        Args:
            id (str): The ID of the file to delete.

        Returns:
            None
        """

        versions = self.get_versions(id)

        for version in versions:
            self._table.update_item(
                Key={
                    "id": version.id,
                    "version": version.version
                },
                UpdateExpression="SET #s = :deleted",
                ExpressionAttributeNames={"#s": "status"},
                ExpressionAttributeValues={":deleted": "DELETED"}
            )


    def save(
        self,
        version: TVersion,
        path: str
    ) -> None:
        """
        Save a file version to the DynamoDB table.

        Args:
            version (TVersion): The file version to save.
            path (str): The storage path of the file.

        Returns:
            None
        """

        data = asdict(version)
        data["storage_path"] = path

        self._table.put_item(Item=data)


    def _deserialize(
        self,
        item: dict
    ) -> TVersion:
        """
        Deserialize a DynamoDB item into a version object.

        Args:
            item (dict): The DynamoDB item to deserialize.

        Returns:
            TVersion: The deserialized version object.
        """

        allowed_fields = self._version_cls.__dataclass_fields__.keys()
        filtered = {k: v for k, v in item.items() if k in allowed_fields}
        return self._version_cls(**filtered)