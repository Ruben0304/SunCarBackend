import os
import uuid
from supabase import create_client, Client

_supabase_client = None

def get_supabase_client() -> Client:
    global _supabase_client
    if _supabase_client is None:
        SUPABASE_URL = os.getenv("SUPABASE_URL")
        SUPABASE_KEY = os.getenv("SUPABASE_KEY")
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise Exception("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _supabase_client

async def upload_file_to_supabase(file_content: bytes, original_filename: str, content_type: str) -> str:
    BUCKET_NAME = os.getenv("SUPABASE_BUCKET", "photos")
    supabase = get_supabase_client()
    file_extension = original_filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"

    response = supabase.storage.from_(BUCKET_NAME).upload(
        path=unique_filename,
        file=file_content,
        file_options={
            "content-type": content_type,
            "upsert": False
        }
    )
    if hasattr(response, "status_code"):
        status_code = response.status_code
    elif isinstance(response, dict) and "status_code" in response:
        status_code = response["status_code"]
    else:
        status_code = 200

    if status_code != 200:
        raise Exception("Error al subir el archivo a Supabase")

    public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(unique_filename)
    return public_url 