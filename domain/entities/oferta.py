from typing import List, Optional
from pydantic import BaseModel, Field


class OfertaElemento(BaseModel):
    categoria: Optional[str] = None
    foto: Optional[str] = None
    descripcion: Optional[str] = None
    cantidad: Optional[int] = None


class Oferta(BaseModel):
    id: Optional[str] = Field(default=None, description="ID de la oferta")
    descripcion: str
    precio: float
    garantias: List[str] = []
    elementos: List[OfertaElemento] = []


