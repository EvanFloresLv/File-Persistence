# ---------------------------------------------------------------------
# Standard library
# ---------------------------------------------------------------------
from datetime import datetime
from typing import Optional, List, Any, Dict

from dataclasses import dataclass


@dataclass(slots=True)
class Lifecycle:
    created_at: datetime
    created_by: str

    updated_at: datetime
    updated_by: str

    deleted_at: Optional[datetime]
    deleted_by: Optional[str]


@dataclass(slots=True)
class Storage:
    bucket: str
    path: str
    uri: str
    size_bytes: int


@dataclass(slots=True)
class Metadata:
    file_name: str
    file_extension: str
    mime_type: str


@dataclass(slots=True)
class Versioning:
    is_latest: bool
    parent_version_id: Any


@dataclass(slots=True)
class FileVersionCustom:
    id: Any
    lifecycle: Lifecycle
    description: Optional[str]

    segmentation_groups: List[str]

    metadata: Metadata
    versioning: Versioning

    version: Any = 1
    status: str = "ACTIVE"


@dataclass(slots=True)
class FileVersionCustomDict:
    id: Any
    lifecycle: Dict[str, datetime | str | None]
    description: Optional[str]
    segmentation_groups: List[str]
    metadata: Dict[str, str]
    status: str = "ACTIVE"