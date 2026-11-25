def list_samples(collection, authenticated_user, body):
    """Return only the authenticated user's samples; body is request JSON."""
    filters = dict(body)
    filters.setdefault("owner_id", authenticated_user["id"])
    return list(collection.find(filters).limit(100))
