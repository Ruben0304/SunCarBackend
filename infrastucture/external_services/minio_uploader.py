import os
import uuid
from minio import Minio
from minio.error import S3Error
from urllib.parse import urlparse

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
        
        # Parse endpoint to extract host and determine if secure
        parsed_url = urlparse(MINIO_ENDPOINT)
        if parsed_url.scheme:
            # Endpoint includes protocol (e.g., http://host:port)
            endpoint_host = parsed_url.netloc
            secure = parsed_url.scheme == 'https'
        else:
            # Endpoint is just host:port
            endpoint_host = MINIO_ENDPOINT
            secure = MINIO_SECURE
        
        _minio_client = Minio(
            endpoint_host,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=secure
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
        MINIO_PUBLIC_ENDPOINT = os.getenv("MINIO_PUBLIC_ENDPOINT", MINIO_ENDPOINT)
        
        # Use public endpoint if available, otherwise use private endpoint
        endpoint_for_url = MINIO_PUBLIC_ENDPOINT
        
        # Parse endpoint to construct proper URL
        parsed_url = urlparse(endpoint_for_url)
        if parsed_url.scheme:
            # Endpoint already includes protocol
            base_url = endpoint_for_url.rstrip('/')
        else:
            # Endpoint is just host:port, add protocol
            MINIO_SECURE = os.getenv("MINIO_SECURE", "False").lower() == "true"
            protocol = "https" if MINIO_SECURE else "http"
            base_url = f"{protocol}://{endpoint_for_url}"
        
        public_url = f"{base_url}/{BUCKET_NAME}/{unique_filename}"
        return public_url
        
    except S3Error as e:
        raise Exception(f"Error uploading file to MinIO: {e}")