from typing import Optional
from pydantic import BaseModel
from domain.entities.cliente import Cliente


class ClienteCreateResponse(BaseModel):
    success: bool
    message: str
    data: Cliente


class ClienteVerifyResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None 