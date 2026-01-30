# Project Name

A file persistence service that uploads files to cloud storage (Google, Amazon, Azure, Self-hosted) and records versioning and timestamp metadata in a NoSQL database (like Firestore). Supports custom dataclass-based objects for structured file metadata ingestion and extensible storage backends.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Overview

This project provides a unified persistence layer for storing files in cloud storage while tracking structured metadata, version history, and timestamps in a NoSQL database.

It is designed to decouple file storage from metadata management, enabling scalable ingestion pipelines, backend services, and AI/data platforms to manage file lifecycle state consistently.

Key design goals:

- Storage backend agnosticism (GCP, AWS, Azure, on-prem)
- Strongly typed metadata using Python dataclasses
- Clean architecture with repository and service layers
- Version-aware file lifecycle management
- Extensibility for enterprise and research workloads

---

## Architecture

The system follows a layered clean architecture to isolate domain logic from infrastructure concerns.

```
Client
    ↓
API / Interface Layer
    ↓
Service Layer
(Domain Logic)
    ↓
Repository Layer
(Persistence Abstractions)
    ↓
NoSQL Database (Metadata) +
Cloud Storage (Files)
```

### Core Components:

1. **API Layer:** Interfaces (CLI, SDK, REST) for uploading and managing files
2. **Service Layer:** Business logic for versioning and lifecycle rules
3. **Repository Layer:** Abstract persistence interfaces for storage and metadata
4. **Infrastructure Layer:** Cloud storage providers and NoSQL database adapters

---

## Features

- Cloud file storage (Google Cloud Storage, Amazon S3, Azure Blob, local/self-hosted)
- NoSQL metadata persistence (Firestore-compatible)
- File versioning with active and historical versions
- Timestamp registry (created, updated, deleted)
- Custom Python dataclass ingestion for typed metadata models
- Pluggable repository pattern for backend extensibility
- Clean Architecture and DDD-inspired design
- Type-safe domain models

---

## Installation
```bash
pip install <url>
```


Or install from source:

```bash
git clone https://github.com/your-org/project-name.git
cd project-name
pip install -e .
```

Usage
```python
from dataclasses import dataclass
from persistence import FileService

@dataclass
class FileMetadata:
    description: str
    owner: str

service = FileService()
service.upload_file(
    path="data/report.pdf",
    metadata=FileMetadata(description="Q4 report", owner="finance")
)
```

---

### Configuration

Configuration is done via environment variables or config files:

```
STORAGE_PROVIDER=gcs
NOSQL_PROVIDER=firestore
BUCKET_NAME=my-bucket
PROJECT_ID=my-project
```

---

### Project Structure

```
src/
 ├── domain/          # Entities, value objects, dataclasses
 ├── services/        # Business logic
 ├── repositories/    # Persistence abstractions
 ├── infrastructure/  # Cloud and NoSQL adapters
 ├── api/             # Interfaces (REST/CLI)
 └── config/          # Configuration files and environment
```
---

### Development
```bash
pip install -r requirements-dev.txt
pre-commit install
```

---

### Testing
```
pytest tests/
```

---

### Deployment

The service can be deployed as:

```
Python SDK library
FastAPI microservice
Serverless function (Cloud Run / Lambda / Azure Functions)
Internal data platform component
```

---

### Roadmap

1. Multi-file batch ingestion
2. Event-driven metadata updates
3. Soft-delete and retention policies
4. Audit logs and lineage tracking
5. Multi-tenant namespace support
6. Web dashboard for file lifecycle visualization

---

### Contributing

Contributions are welcome.
Please follow the coding standards and submit PRs with tests and documentation updates.

---

### License

MIT License.

---

### Contact

Maintainer: Evan Flores
Email: *efloresp06@liverpool.com.mx*
Organization: **Liverpool**