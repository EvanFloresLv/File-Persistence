if __name__ == "__main__":

    from datetime import datetime
    from uuid import uuid4

    from src.application.use_cases import FileService

    from src.infrastructure.google.firestore import FirestoreFileMetadataRepository
    from src.infrastructure.google.gcs import GCSStorage
    from src.infrastructure.google.clients import gcs_client, firestore_client

    from src.examples.custom_entities import Lifecycle, Metadata, Versioning, FileVersionCustom

    gcs = gcs_client()
    fs = firestore_client()

    bucket = gcs.bucket("crp-dev-sis-cari2-bkt01")
    collection = fs.collection("test")

    id = str(uuid4())

    fs = FileService(
        repository=FirestoreFileMetadataRepository(
            collection=collection,
            version_cls=FileVersionCustom
        ),
        storage=GCSStorage(bucket),
        base_path="test"
    )

    fs.create(
        content=b"PDF CONTENT",
        content_type="application/pdf",
        version=FileVersionCustom(
            id=id,
            version=1,
            status="ACTIVE",
            lifecycle=Lifecycle(
                created_at=datetime.now(),
                created_by="user_1",
                updated_at=datetime.now(),
                updated_by="user_1",
                deleted_at=None,
                deleted_by=None
            ),
            description="Sample file version",
            segmentation_groups=["group1", "group2"],
            metadata=Metadata(
                file_name="sample.pdf",
                file_extension=".pdf",
                mime_type="application/pdf",
            ),
            versioning=Versioning(
                is_latest=True,
                parent_version_id=None
            )
        )
    )

    fs.update(
        content=b"NEW PDF CONTENT",
        content_type="application/pdf",
        version=FileVersionCustom(
            id=id,
            status="ACTIVE",
            lifecycle=Lifecycle(
                created_at=datetime.now(),
                created_by="user_1",
                updated_at=datetime.now(),
                updated_by="user_1",
                deleted_at=None,
                deleted_by=None
            ),
            description="Sample file version",
            segmentation_groups=["group1", "group2"],
            metadata=Metadata(
                file_name="sample.pdf",
                file_extension=".pdf",
                mime_type="application/pdf",
            ),
            versioning=Versioning(
                is_latest=True,
                parent_version_id=None
            )
        )
    )