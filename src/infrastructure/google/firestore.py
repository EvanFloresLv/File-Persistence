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
    """
    Firestore implementation of the FileMetadataRepository interface.
    """

    def __init__(
        self,
        collection,
        version_cls: Type[TVersion]
    ):
        """
        Initialize the FirestoreFileMetadataRepository with a Firestore collection and a version class.

        Args:
            collection: The Firestore collection to use.
            version_cls (Type[TVersion]): The version class to use for deserialization.

        Returns:
            None
        """

        self._collection = collection
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
        """
        Get all versions of a file by its ID.

        Args:
            id (str): The ID of the file to retrieve.

        Returns:
            List[TVersion]: A list of all versions of the file.
        """

        docs = self._collection.where(
            filter=FieldFilter("id", "==", id)
        ).stream()

        return [self._version_cls(**doc.to_dict()) for doc in docs]


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
        """
        Delete all versions of a file by its ID.

        Args:
            id (str): The ID of the file to delete.

        Returns:
            None
        """

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
        """
        Save a file version to Firestore.

        Args:
            version (TVersion): The file version to save.
            path (str): The storage path of the file.

        Returns:
            None
        """

        data = asdict(version)
        data["storage_path"] = path
        self._collection.add(data)


    def _deserialize(
        self,
        item: dict
    ) -> TVersion:
        """
        Deserialize a Firestore document into a version object.

        Args:
            item (dict): The Firestore document data.

        Returns:
            TVersion: The deserialized version object.
        """

        allowed_fields = self._version_cls.__dataclass_fields__.keys()
        filtered = {k: v for k, v in item.items() if k in allowed_fields}
        return self._version_cls(**filtered)
