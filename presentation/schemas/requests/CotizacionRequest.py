from pydantic import BaseModel


class CotizacionRequest(BaseModel):
    mensaje: str 