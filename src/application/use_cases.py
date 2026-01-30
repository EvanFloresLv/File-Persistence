# ---------------------------------------------------------------------
# Internal application imports
# ---------------------------------------------------------------------
import dataclasses
from typing import Generic, TypeVar
from src.domain.repositories import FileMetadataRepository, FileStorage


TVersion = TypeVar("TVersion")


class FileService(Generic[TVersion]):
    """
    Service for managing file versions.
    """

    def __init__(
        self,
        repository: FileMetadataRepository[TVersion],
        storage: FileStorage,
        *,
        base_path: str | None = None,
    ):
        """
        Initialize the FileService.

        Args:
            repository (FileMetadataRepository[TVersion]): The file metadata repository.
            storage (FileStorage): The file storage.
            base_path (str | None): The base path for file storage.

        Returns:
            None
        """

        self._repository = repository
        self._storage = storage
        self._base_path = base_path.strip("/") if base_path else None

    # ------------------------------------------------------------------
    # Path handling (generic)
    # ------------------------------------------------------------------

    def _build_path(
        self,
        id: str,
        version: int | str
    ) -> str:
        """
        Build the storage path for a file version.

        Args:
            id (str): The ID of the file.
            version (int | str): The version of the file.

        Returns:
            str: The constructed storage path.
        """

        try:
            parts = []
            if self._base_path:
                parts.append(self._base_path)
            parts.append(id)
            if str(version):
                parts.append(f"v{version}")
            return "/".join(parts)
        except Exception as exc:
            print(f"Error building path: {exc}")

    # ------------------------------------------------------------------
    # Validation (minimal & generic)
    # ------------------------------------------------------------------

    def _validate(
        self,
        version: TVersion
    ) -> None:
        """
        Validate the file version.

        Args:
            version (TVersion): The file version to validate.

        Returns:
            None
        """

        try:
            for field in ("id", "version", "status"):
                if not getattr(version, field, None):
                    raise ValueError(f"{field} is required")
        except Exception as exc:
            print(f"Error validating version: {exc}")

    # ------------------------------------------------------------------
    # Use cases
    # ------------------------------------------------------------------

    def create(
        self,
        *,
        content: bytes,
        content_type: str,
        version: TVersion,
    ) -> None:
        """
        Create a new file version.

        Args:
            content (bytes): The content of the file.
            content_type (str): The MIME type of the file.
            version (TVersion): The version metadata.

        Returns:
            None
        """

        try:
            self._validate(version)

            path = self._build_path(version.id, version.version)

            self._storage.upload(path, content, content_type)
            self._repository.save(version=version, path=path)
        except Exception as exc:
            print(f"Error creating file: {exc}")


    def get_active(
        self,
        id: str
    ) -> TVersion | None:
        """
        Get the active version of a file.

        Args:
            id (str): The ID of the file.

        Returns:
            TVersion | None: The active version of the file, or None if not found.
        """

        try:
            return self._repository.get_active(id)
        except Exception as exc:
            print(f"Error getting active version: {exc}")


    def update(
        self,
        *,
        content: bytes,
        content_type: str,
        version: TVersion,
    ) -> None:
        """
        Update an existing file version.

        Args:
            content (bytes): The new content of the file.
            content_type (str): The new MIME type of the file.
            version (TVersion): The version metadata.

        Returns:
            None
        """

        try:
            self._validate(version)

            active = self._repository.get_active(version.id)

            if not active:
                return

            next_version = active.version + 1 if active else 1

            new_version = self._clone_version(
                version,
                version=next_version,
                status="ACTIVE",
            )

            path = self._build_path(version.id, next_version)

            self._repository.deactivate_versions(version.id)
            self._storage.upload(path, content, content_type)
            self._repository.save(version=new_version, path=path)
        except Exception as exc:
            print(f"Error updating file: {exc}")


    def delete(
        self,
        id: str, *,
        physical: bool = False
    ) -> None:
        """
        Delete a file version.

        Args:
            id (str): The ID of the file.
            physical (bool): Whether to delete the file physically from storage.

        Returns:
            None
        """

        try:
            active = self._repository.get_active(id)

            if not active:
                return

            self._repository.delete_versions(id)

            if physical:
                self._storage.delete(self._build_path(id, ""))
        except Exception as exc:
            print(f"Error deleting file: {exc}")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _clone_version(
        self,
        obj: TVersion,
        **changes
    ) -> TVersion:
        """
        Clone a version object with updated fields.

        Args:
            obj (TVersion): The original version object.
            **changes: The fields to update in the cloned object.

        Returns:
            TVersion: The cloned version object.
        """

        try:
            if dataclasses.is_dataclass(obj):
                data = dataclasses.asdict(obj)
            elif hasattr(obj, "__dict__"):
                data = vars(obj).copy()
            elif hasattr(obj, "_asdict"):
                data = obj._asdict()
            else:
                raise TypeError("Unsupported version object type for cloning")

            data.update(changes)
            return type(obj)(**data)
        except Exception as exc:
            print(f"Error cloning version: {exc}")