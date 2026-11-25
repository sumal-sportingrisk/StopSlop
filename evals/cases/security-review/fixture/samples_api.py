def search_samples(collection, owner_id, body):
    """List the caller's samples. owner_id comes from the session; body is the request JSON."""
    criteria = {"owner_id": owner_id}
    criteria.update(body)
    return list(collection.find(criteria))
