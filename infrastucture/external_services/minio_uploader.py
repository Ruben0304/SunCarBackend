import os
import uuid
from minio import Minio
from minio.error import S3Error
from urllib.parse import urljoin

_minio_client = None

def get_minio_client() -> Minio:
    global _minio_client
    if _minio_client is None:
        MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
        MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
        MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
        MINIO_SECURE = os.getenv("MINIO_SECURE", "False").lower() == "true"
        
        if not MINIO_ENDPOINT or not MINIO_ACCESS_KEY or not MINIO_SECRET_KEY:
            raise Exception("MINIO_ENDPOINT, MINIO_ACCESS_KEY and MINIO_SECRET_KEY must be set in environment variables")
        
        _minio_client = Minio(
            MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=MINIO_SECURE
        )
    return _minio_client

async def upload_file_to_minio(file_content: bytes, original_filename: str, content_type: str) -> str:
    BUCKET_NAME = os.getenv("MINIO_BUCKET", "photos")
    minio_client = get_minio_client()
    
    # Ensure bucket exists
    try:
        if not minio_client.bucket_exists(BUCKET_NAME):
            minio_client.make_bucket(BUCKET_NAME)
    except S3Error as e:
        raise Exception(f"Error creating/accessing bucket: {e}")
    
    # Generate unique filename
    file_extension = original_filename.split(".")[-1] if "." in original_filename else "bin"
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    
    try:
        # Upload file
        from io import BytesIO
        file_stream = BytesIO(file_content)
        
        minio_client.put_object(
            bucket_name=BUCKET_NAME,
            object_name=unique_filename,
            data=file_stream,
            length=len(file_content),
            content_type=content_type
        )
        
        # Generate public URL
        MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
        MINIO_SECURE = os.getenv("MINIO_SECURE", "False").lower() == "true"
        protocol = "https" if MINIO_SECURE else "http"
        
        public_url = f"{protocol}://{MINIO_ENDPOINT}/{BUCKET_NAME}/{unique_filename}"
        return public_url
        
    except S3Error as e:
        raise Exception(f"Error uploading file to MinIO: {e}")