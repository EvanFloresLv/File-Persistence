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
        docs = (
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

        for doc in docs:
            doc_dict = doc.to_dict()
            allowed_fields = set(f.name for f in self._version_cls.__dataclass_fields__.values())
            filtered_dict = {k: v for k, v in doc_dict.items() if k in allowed_fields}
            return self._version_cls(**filtered_dict)

        return None


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
