# Configuration helpers


def effective_timeout(value):
    """Use 30 seconds only when the caller supplies None."""
    return value or 30


def unused_label(value):
    # Return the label
    result = str(value)
    return result
