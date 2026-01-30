# ---------------------------------------------------------------------
# Internal application imports
# ---------------------------------------------------------------------
import dataclasses
from typing import Generic, TypeVar
from src.domain.repositories import FileMetadataRepository, FileStorage


TVersion = TypeVar("TVersion")


class FileService(Generic[TVersion]):

    def __init__(
        self,
        repository: FileMetadataRepository[TVersion],
        storage: FileStorage,
        *,
        base_path: str | None = None,
    ):
        self._repository = repository
        self._storage = storage
        self._base_path = base_path.strip("/") if base_path else None

    # ------------------------------------------------------------------
    # Path handling (generic)
    # ------------------------------------------------------------------

    def _build_path(self, id: str, version: int | str) -> str:
        parts = []
        if self._base_path:
            parts.append(self._base_path)
        parts.append(id)
        if str(version):
            parts.append(f"v{version}")
        return "/".join(parts)

    # ------------------------------------------------------------------
    # Validation (minimal & generic)
    # ------------------------------------------------------------------

    def _validate(self, version: TVersion) -> None:
        for field in ("id", "version", "status"):
            if not getattr(version, field, None):
                raise ValueError(f"{field} is required")

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
        self._validate(version)

        path = self._build_path(version.id, version.version)

        self._storage.upload(path, content, content_type)
        self._repository.save(version=version, path=path)


    def get_active(self, id: str) -> TVersion | None:
        return self._repository.get_active(id)


    def update(
        self,
        *,
        content: bytes,
        content_type: str,
        version: TVersion,
    ) -> None:
        self._validate(version)

        active = self._repository.get_active(version.id)

        if not active:
            raise ValueError("No active version found")

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


    def delete(self, id: str, *, physical: bool = False) -> None:
        active = self._repository.get_active(id)

        if not active:
            return

        self._repository.delete_versions(id)

        if physical:
            self._storage.delete(self._build_path(id, ""))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _clone_version(self, obj: TVersion, **changes) -> TVersion:
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