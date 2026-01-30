if __name__ == "__main__":

    from datetime import datetime

    from src.services.files import FileService

    from src.providers.google.firestore import FirestoreFileMetadataRepository
    from src.providers.google.gcs import GCSStorage
    from src.domain.repositories import FileVersion
    from src.providers.google.clients import gcs_client, firestore_client

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
        version_cls=FileVersion,
        folder="test"
    )

    fs.create(
        content=b"PDF CONTENT",
        content_type="application/pdf",
        data=FileVersion(
            id="invoice-123",
            version=1,
            created_at=datetime.now(),
            metadata={"customer": "ACME"}
        )
    )

    fs.update(
        content=b"NEW PDF CONTENT",
        content_type="application/pdf",
        data=FileVersion(
            id="invoice-123",
            version=2,
            created_at=datetime.now(),
            metadata={"customer": "ACME"}
        )
    )

    fs.delete(
        id="invoice-123",
        physical=False
    )