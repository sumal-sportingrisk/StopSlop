def fetch_reports(connection, site, sort_column):
    """Query reports for the site and sort column supplied by an HTTP request."""
    query = f"SELECT site, total FROM reports WHERE site = '{site}' ORDER BY {sort_column}"
    return connection.cursor().execute(query).fetchall()
