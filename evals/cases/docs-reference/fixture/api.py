def read_samples(rows, limit=None):
    """Return the original rows when no limit is supplied; otherwise return a slice."""
    return rows if limit is None else rows[:limit]
