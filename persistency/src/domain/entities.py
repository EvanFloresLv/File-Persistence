# ---------------------------------------------------------------------
# Standard library
# ---------------------------------------------------------------------
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Protocol, runtime_checkable


@runtime_checkable
class VersionedEntity(Protocol):
    id: str
    status: str


@dataclass(slots=True)
class File:
    id: str
    filename: str
    content_type: str
    metadata: Dict[str, str]


@dataclass(slots=True)
class FileVersion:
    id: str
    created_at: datetime
    metadata: Dict[str, str]
    status: str = "ACTIVE"
    version: int = 1