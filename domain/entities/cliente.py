from pydantic import BaseModel
from typing import Optional


class Cliente(BaseModel):
    numero: str
    nombre: str
    direccion: str
    latitud: str
    longitud: str
    telefono: Optional[str] = None 