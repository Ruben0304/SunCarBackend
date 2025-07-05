from typing import List, Optional
from pydantic import BaseModel
from domain.entities.brigada import Brigada


class BrigadaListResponse(BaseModel):
    success: bool
    message: str
    data: List[Brigada]


class BrigadaDetailResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Brigada] = None


class BrigadaCreateResponse(BaseModel):
    success: bool
    message: str
    brigada_id: str


class BrigadaUpdateResponse(BaseModel):
    success: bool
    message: str


class BrigadaDeleteResponse(BaseModel):
    success: bool
    message: str


class BrigadaMemberResponse(BaseModel):
    success: bool
    message: str 