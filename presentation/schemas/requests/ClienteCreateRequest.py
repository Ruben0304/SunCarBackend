from pydantic import BaseModel
from typing import Optional


class ClienteCreateRequest(BaseModel):
    numero: str
    nombre: str
    direccion: str
    latitud: str
    longitud: str 


class ClienteCreateSimpleRequest(BaseModel):
    numero: str
    nombre: str
    direccion: str
    latitud: Optional[str] = None
    longitud: Optional[str] = None 