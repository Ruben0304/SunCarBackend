from pydantic import BaseModel
from typing import Optional


class LeadCreateRequest(BaseModel):
    fecha_contacto: str
    nombre: str
    telefono: str
    estado: str
    fuente: Optional[str] = None
    referencia: Optional[str] = None
    direccion: Optional[str] = None
    pais_contacto: Optional[str] = None
    necesidad: Optional[str] = None
    provincia_montaje: Optional[str] = None


class LeadUpdateRequest(BaseModel):
    fecha_contacto: Optional[str] = None
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    estado: Optional[str] = None
    fuente: Optional[str] = None
    referencia: Optional[str] = None
    direccion: Optional[str] = None
    pais_contacto: Optional[str] = None
    necesidad: Optional[str] = None
    provincia_montaje: Optional[str] = None