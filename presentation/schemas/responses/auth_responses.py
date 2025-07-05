from typing import Optional
from pydantic import BaseModel
from domain.entities.brigada import Brigada


class LoginResponse(BaseModel):
    success: bool
    message: str
    brigada: Optional[Brigada] = None


class ChangePasswordResponse(BaseModel):
    success: bool
    message: str 