from typing import List, Optional
from pydantic import BaseModel
from domain.entities.oferta import Oferta, OfertaSimplificada


class OfertasListResponse(BaseModel):
    success: bool
    message: str
    data: List[Oferta]


class OfertaGetResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Oferta] = None


class OfertaCreateResponse(BaseModel):
    success: bool
    message: str
    oferta_id: str


class OfertaUpdateResponse(BaseModel):
    success: bool
    message: str


class OfertaDeleteResponse(BaseModel):
    success: bool
    message: str


class OfertasSimplificadasListResponse(BaseModel):
    success: bool
    message: str
    data: List[OfertaSimplificada]


class ElementoAddResponse(BaseModel):
    success: bool
    message: str


class ElementoDeleteResponse(BaseModel):
    success: bool
    message: str


class ElementoUpdateResponse(BaseModel):
    success: bool
    message: str


