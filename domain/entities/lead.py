from pydantic import BaseModel
from typing import Optional


class Lead(BaseModel):
    id: Optional[str] = None
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