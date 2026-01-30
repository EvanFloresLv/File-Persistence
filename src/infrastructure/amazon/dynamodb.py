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

    def __init__(
        self,
        table,
        version_cls: Type[TVersion]
    ):
        self._table = table
        self._version_cls = version_cls


    def get_active(
        self,
        id: str
    ) -> Optional[TVersion]:
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
        data = asdict(version)
        data["storage_path"] = path

        self._table.put_item(Item=data)


    def _deserialize(
        self,
        item: dict
    ) -> TVersion:
        allowed_fields = self._version_cls.__dataclass_fields__.keys()
        filtered = {k: v for k, v in item.items() if k in allowed_fields}
        return self._version_cls(**filtered)