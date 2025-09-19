from typing import List, Optional
from pydantic import BaseModel, Field


class OfertaElemento(BaseModel):
    categoria: Optional[str] = None
    descripcion: str
    cantidad: float = Field(..., gt=0, description="Cantidad debe ser mayor a 0")
    foto: Optional[str] = Field(default=None, description="URL de la foto del elemento")


class Oferta(BaseModel):
    id: Optional[str] = Field(default=None, description="ID de la oferta")
    descripcion: str
    precio: float
    precio_cliente: Optional[float] = Field(default=None, description="Precio específico para el cliente")
    imagen: Optional[str] = Field(default=None, description="URL de imagen de la oferta")
    garantias: List[str] = []
    elementos: List[OfertaElemento] = []


class OfertaSimplificada(BaseModel):
    id: Optional[str] = Field(default=None, description="ID de la oferta")
    descripcion: str
    precio: float
    precio_cliente: Optional[float] = Field(default=None, description="Precio específico para el cliente")
    imagen: Optional[str] = Field(default=None, description="URL de imagen de la oferta")


