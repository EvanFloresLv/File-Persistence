# ---------------------------------------------------------------------
# Standard library
# ---------------------------------------------------------------------
from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic

# ---------------------------------------------------------------------
# Internal application imports
# ---------------------------------------------------------------------
from src.domain.entities import FileVersion

TVersion = TypeVar("TVersion", bound=FileVersion)

class FileMetadataRepository(Generic[TVersion]):
    """
    Interface for file metadata storage and retrieval.
    """

    @abstractmethod
    def get_active(self, id: str) -> Optional[TVersion]:
        """
        Get the active version of a file by its ID.

        Args:
            id (str): The ID of the file to get the active version for.
        """
        raise NotImplementedError

    @abstractmethod
    def get_versions(self, id: str) -> List[TVersion]:
        """
        Get all versions of a file by its ID.

        Args:
            id (str): The ID of the file to get versions for.
        """
        raise NotImplementedError

    @abstractmethod
    def save(self, version: TVersion) -> None:
        """
        Save a file version.

        Args:
            version (TVersion): The file version to save.
        """
        raise NotImplementedError

    @abstractmethod
    def deactivate_versions(self, id: str) -> None:
        """
        Deactivate all versions of a file by its ID.

        Args:
            id (str): The ID of the file to deactivate versions for.
        """
        raise NotImplementedError

    @abstractmethod
    def delete_versions(self, id: str) -> None:
        """
        Delete all versions of a file by its ID.

        Args:
            id (str): The ID of the file to delete versions for.
        """
        raise NotImplementedError


class FileStorage(ABC):

    @abstractmethod
    def upload(self, path: str, content: bytes, content_type: str) -> None:
        """
        Upload a file to the storage.

        Args:
            path (str): The path to the file to upload.
            content (bytes): The content of the file to upload.
            content_type (str): The content type of the file to upload.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, path: str) -> None:
        """
        Delete a file from the storage.

        Args:
            path (str): The path to the file to delete.
        """
        raise NotImplementedError
