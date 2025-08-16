from pydantic import BaseModel
from typing import Optional


class CotizacionRequest(BaseModel):
    mensaje: str
    latitud: Optional[float] = None
    longitud: Optional[float] = None 