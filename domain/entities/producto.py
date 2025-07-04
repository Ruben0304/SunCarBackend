from datetime import datetime, timezone
from pydantic import BaseModel,Field
from typing import List

class MaterialConFecha(BaseModel):
    codigo: str
    descripcion: str
    um: str
    fechaCreacion: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Fecha y hora de creación del material en UTC"
    )

class Material(BaseModel):
    codigo: str
    descripcion: str
    um: str


class CatalogoProductos(BaseModel):
    id: str = None
    categoria: str
    materiales: List[Material]

class Cataegoria(BaseModel):
    id: str = None
    categoria: str
