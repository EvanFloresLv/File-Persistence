# ---------------------------------------------------------------------
# Third-party libraries
# ---------------------------------------------------------------------
from google.auth import default
from google.cloud import firestore, storage


def firestore_client():
    credentials, project = default()
    return firestore.Client(
        credentials=credentials,
        project=project
    )


def gcs_client():
    credentials, project = default()
    return storage.Client(
        credentials=credentials,
        project=project
    )
