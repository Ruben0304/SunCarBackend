from pydantic import BaseModel


class ClienteCreateRequest(BaseModel):
    numero: str
    nombre: str
    direccion: str
    latitud: str
    longitud: str 