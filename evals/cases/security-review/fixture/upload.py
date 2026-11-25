import boto3

# Uploads nightly exports to the reports bucket.
s3 = boto3.client(
    "s3",
    aws_access_key_id="AKIAIOSFODNN7EXAMPLE",
    aws_secret_access_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
)


def upload_export(path, key):
    s3.upload_file(str(path), "lab-reports", f"exports/{key}")
