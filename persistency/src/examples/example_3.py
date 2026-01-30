if __name__ == "__main__":

    from datetime import datetime
    from uuid import uuid4

    from src.services.files import FileService

    from src.providers.google.firestore import FirestoreFileMetadataRepository
    from src.providers.google.gcs import GCSStorage
    from src.providers.google.clients import gcs_client, firestore_client

    from src.domain.file import FileVersionCustomDict

    gcs = gcs_client()
    fs = firestore_client()

    bucket = gcs.bucket("crp-dev-sis-cari2-bkt01")
    collection = fs.collection("test")

    fs = FileService(
        repository=FirestoreFileMetadataRepository(
            collection=collection,
            version_cls=FileVersionCustomDict
        ),
        storage=GCSStorage(bucket),
        version_cls=FileVersionCustomDict,
        folder="test"
    )

    fs.create(
        content=b"PDF CONTENT",
        content_type="application/pdf",
        data=FileVersionCustomDict(
            id=str(uuid4()),
            status="ACTIVE",
            lifecycle={
                "created_at": datetime.now(),
                "created_by": "user_1",
                "updated_at": datetime.now(),
                "updated_by": "user_1",
                "deleted_at": None,
                "deleted_by": None
            },
            description="Sample file version",
            segmentation_groups=["group1", "group2"],
            metadata={
                "file_name": "sample.pdf",
                "file_extension": ".pdf",
                "mime_type": "application/pdf",
            },
        )
    )