from google.cloud import storage
import os

def upload_file_to_gcs(file, filename, content_type):
    bucket_name = os.getenv("GCP_BUCKET_NAME")
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(filename)
    blob.upload_from_file(file, content_type=content_type)
    return f"https://storage.googleapis.com/{bucket_name}/{filename}"