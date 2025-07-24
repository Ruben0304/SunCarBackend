from pydantic import BaseModel
from typing import Optional

class ClienteUpdateRequest(BaseModel):
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    latitud: Optional[str] = None
    longitud: Optional[str] = None 