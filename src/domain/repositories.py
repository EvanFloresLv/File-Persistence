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

    @abstractmethod
    def get_active(self, id: str) -> Optional[TVersion]:
        pass

    @abstractmethod
    def get_versions(self, id: str) -> List[TVersion]:
        pass

    @abstractmethod
    def save(self, version: TVersion) -> None:
        pass

    @abstractmethod
    def deactivate_versions(self, id: str) -> None:
        pass

    @abstractmethod
    def delete_versions(self, id: str) -> None:
        pass


class FileStorage(ABC):

    @abstractmethod
    def upload(self, path: str, content: bytes, content_type: str) -> None:
        pass

    @abstractmethod
    def delete(self, path: str) -> None:
        pass
