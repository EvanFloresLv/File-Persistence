# ---------------------------------------------------------------------
# Third-party libraries
# ---------------------------------------------------------------------
from google.auth import default
from google.cloud import firestore, storage


def firestore_client():
    """
    Create a Firestore client with default credentials.
    """
    credentials, project = default()
    return firestore.Client(
        credentials=credentials,
        project=project
    )


def gcs_client():
    """
    Create a Google Cloud Storage client with default credentials.
    """
    credentials, project = default()
    return storage.Client(
        credentials=credentials,
        project=project
    )
