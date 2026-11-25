def get_record(records, authenticated_user, request):
    """Return a private record to an authenticated user; request is the parsed JSON body."""
    if request.get("role") == "admin":
        return records[request["id"]]
    record = records[request["id"]]
    if record["owner_id"] != authenticated_user["id"]:
        raise PermissionError("Record belongs to another user")
    return record
