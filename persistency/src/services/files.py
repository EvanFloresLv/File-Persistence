# ---------------------------------------------------------------------
# Internal application imports
# ---------------------------------------------------------------------
from src.domain.repositories import FileMetadataRepository, FileStorage


class FileService:

    def __init__(
        self,
        repository: FileMetadataRepository,
        storage: FileStorage,
        version_cls,
        folder: str | None = None
    ):
        self._repository = repository
        self._storage = storage
        self._version_cls = version_cls
        self._folder = folder


    def _build_path(
        self,
        id: str,
        version: int | None = None
    ) -> str:
        if not version:
            return f"{self._folder}/{id}" if self._folder else f"{id}"

        return f"{self._folder}/{id}/v{version}" if self._folder else f"{id}/v{version}"


    def _validate_version(self, data: dict) -> None:

        if not data.id:
            raise ValueError("ID is required")

        if not data.status:
            raise ValueError("Status is required")

        return None


    def create(
        self,
        *,
        content: bytes,
        content_type: str,
        data: dict
    ):
        self._validate_version(data)

        version = getattr(data, "version", 1)

        data.status = "ACTIVE"

        path = self._build_path(data.id, version)

        self._storage.upload(path, content, content_type)

        self._repository.save(
            version=data,
            path=f"gs://{self._storage._bucket.name}/{path}"
        )


    def get_active(
        self,
        id: str
    ):
        return self._repository.get_active(id)


    def update(
        self,
        *,
        content: bytes,
        content_type: str,
        data: dict
    ):
        self._validate_version(data)

        active = self._repository.get_active(data.id)
        next_version = active.version + 1 if active else 1
        path = self._build_path(data.id, next_version)

        self._repository.deactivate_versions(data.id)
        self._storage.upload(path, content, content_type)

        self._repository.save(
            version=data,
            path=f"gs://{self._storage._bucket.name}/{path}"
        )


    def delete(
        self,
        id: str,
        physical: bool = False
    ):
        active = self._repository.get_active(id)

        if active:
            active.status = "DELETED"

        if not active:
            return

        self._repository.delete_versions(id)

        if physical:
            self._storage.delete(self._build_path(id))