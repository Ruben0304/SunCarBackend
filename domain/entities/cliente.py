from pydantic import BaseModel
from typing import Optional


class Cliente(BaseModel):
    numero: str
    nombre: str
    direccion: str
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    telefono: Optional[str] = None 