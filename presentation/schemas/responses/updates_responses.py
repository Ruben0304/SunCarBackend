from typing import Optional
from pydantic import BaseModel
from domain.entities.update import DataUpdateResponse, AppUpdateResponse


class UpdateStatusResponse(BaseModel):
    system_status: str
    last_check: str
    available_entities: list
    app_versions: dict 