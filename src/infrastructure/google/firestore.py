# ---------------------------------------------------------------------
# Standard library
# ---------------------------------------------------------------------
from typing import List, Optional, Type, TypeVar
from dataclasses import asdict

# ---------------------------------------------------------------------
# Third-party library imports
# ---------------------------------------------------------------------
from google.cloud.firestore_v1 import FieldFilter, And

# ---------------------------------------------------------------------
# Internal application imports
# ---------------------------------------------------------------------
from src.domain.repositories import FileMetadataRepository


TVersion = TypeVar("TVersion")


class FirestoreFileMetadataRepository(FileMetadataRepository):

    def __init__(
        self,
        collection,
        version_cls: Type[TVersion]
    ):
        self._collection = collection
        self._version_cls = version_cls


    def get_active(
        self,
        id: str
    ) -> Optional[TVersion]:
        docs = list(
            self._collection
            .where(
                filter=And(
                    [
                        FieldFilter("id", "==", id),
                        FieldFilter("status", "==", "ACTIVE"),
                    ]
                )
            )
            .limit(1)
            .stream()
        )

        if not docs:
            return None

        doc_dict = docs[0].to_dict()
        return self._deserialize(doc_dict)


    def get_versions(
        self,
        id: str
    ) -> List[TVersion]:
        docs = self._collection.where(
            filter=FieldFilter("id", "==", id)
        ).stream()

        return [self._version_cls(**doc.to_dict()) for doc in docs]


    def deactivate_versions(
        self,
        id: str
    ) -> None:
        docs = self._collection.where(
            filter=And(
                [
                    FieldFilter("id", "==", id),
                    FieldFilter("status", "==", "ACTIVE"),
                ]
            )
        ).stream()

        for doc in docs:
            doc.reference.update({"status": "INACTIVE"})


    def delete_versions(
        self,
        id: str
    ) -> None:
        docs = self._collection.where(
            filter=FieldFilter("id", "==", id)
        ).stream()

        for doc in docs:
            doc.reference.update({"status": "DELETED"})


    def save(
        self,
        version: TVersion,
        path: str
    ) -> None:
        data = asdict(version)
        data["storage_path"] = path
        self._collection.add(data)


    def _deserialize(
        self,
        item: dict
    ) -> TVersion:
        allowed_fields = self._version_cls.__dataclass_fields__.keys()
        filtered = {k: v for k, v in item.items() if k in allowed_fields}
        return self._version_cls(**filtered)
