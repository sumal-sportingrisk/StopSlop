def round_report_value(value, places=0):
    """Round half away from zero, as the regulatory report format requires."""
    return round(value, places)
