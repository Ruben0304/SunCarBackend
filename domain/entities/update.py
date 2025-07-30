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
    
    def model_post_init(self, __context) -> None:
        """Validate the current_version format"""
        if not self.current_version or self.current_version.strip() == "":
            raise ValueError("current_version cannot be empty")
        if self.current_version.lower() == "string":
            raise ValueError("current_version cannot be the literal string 'string'")


class AppUpdateResponse(BaseModel):
    is_up_to_date: bool
    latest_version: Optional[str] = None
    download_url: Optional[str] = None
    file_size: Optional[int] = None  # en bytes
    changelog: Optional[str] = None
    force_update: bool = False  # si es obligatorio actualizar


class AppVersionConfig(BaseModel):
    """
    Entidad para almacenar configuración de versiones de app en MongoDB
    """
    id: Optional[str] = None
    platform: str  # android, ios
    latest_version: str
    download_url: str
    file_size: int  # en bytes
    changelog: str
    force_update: bool = False
    min_version: str  # versión mínima requerida
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None 