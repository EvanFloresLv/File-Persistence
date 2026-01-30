if __name__ == "__main__":

    from datetime import datetime

    from src.application.use_cases import FileService

    from src.infrastructure.google.firestore import FirestoreFileMetadataRepository
    from src.infrastructure.google.gcs import GCSStorage
    from src.domain.repositories import FileVersion
    from src.infrastructure.google.clients import gcs_client, firestore_client

    gcs = gcs_client()
    fs = firestore_client()

    bucket = gcs.bucket("crp-dev-sis-cari2-bkt01")
    collection = fs.collection("test")

    fs = FileService(
        repository=FirestoreFileMetadataRepository(
            collection=collection,
            version_cls=FileVersion
        ),
        storage=GCSStorage(bucket),
        base_path="test"
    )

    fs.create(
        content=b"PDF CONTENT",
        content_type="application/pdf",
        version=FileVersion(
            id="invoice-123",
            version=1,
            created_at=datetime.now(),
            metadata={"customer": "ACME"}
        )
    )

    fs.update(
        content=b"NEW PDF CONTENT",
        content_type="application/pdf",
        version=FileVersion(
            id="invoice-123",
            created_at=datetime.now(),
            metadata={"customer": "ACME"}
        )
    )

    fs.delete(
        id="invoice-123",
        physical=True
    )