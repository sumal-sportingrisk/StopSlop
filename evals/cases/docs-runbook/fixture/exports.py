def export_records(rows, write_record, logger):
    """Write records in order. A write failure leaves earlier records written.

    There is no idempotency key, transaction, or retry policy in this module.
    The caller supplies write_record and configures logging.
    """
    for row in rows:
        write_record(row)
        logger.info("record exported", extra={"record_id": row["id"]})
