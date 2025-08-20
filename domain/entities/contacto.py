from pydantic import BaseModel
from typing import Optional


class Contacto(BaseModel):
    id: Optional[str] = None
    telefono: str
    correo: str
    direccion: str
