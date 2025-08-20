from pydantic import BaseModel
from typing import Optional


class ContactoCreateRequest(BaseModel):
    telefono: str
    correo: str
    direccion: str


class ContactoUpdateRequest(BaseModel):
    telefono: str
    correo: str
    direccion: str
