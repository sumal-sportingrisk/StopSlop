import pickle


def load_upload(uploaded_bytes):
    """Accept the bytes of a model file uploaded by any authenticated user."""
    return pickle.loads(uploaded_bytes)
