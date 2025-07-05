from typing import List, Optional
from pydantic import BaseModel
from domain.entities.trabajador import Trabajador


class TrabajadorListResponse(BaseModel):
    success: bool
    message: str
    data: List[Trabajador]


class TrabajadorDetailResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Trabajador] = None


class TrabajadorCreateResponse(BaseModel):
    success: bool
    message: str
    trabajador_id: str


class TrabajadorUpdateResponse(BaseModel):
    success: bool
    message: str


class TrabajadorSearchResponse(BaseModel):
    success: bool
    message: str
    data: List[Trabajador]


class TrabajadorBrigadaResponse(BaseModel):
    success: bool
    message: str 