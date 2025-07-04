from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class DataUpdateRequest(BaseModel):
    last_update_timestamp: datetime


class DataUpdateResponse(BaseModel):
    is_up_to_date: bool
    outdated_entities: List[str] = []
    current_timestamp: datetime


class AppUpdateRequest(BaseModel):
    current_version: str
    platform: str = "android"  # android, ios


class AppUpdateResponse(BaseModel):
    is_up_to_date: bool
    latest_version: Optional[str] = None
    download_url: Optional[str] = None
    file_size: Optional[int] = None  # en bytes
    changelog: Optional[str] = None
    force_update: bool = False  # si es obligatorio actualizar 