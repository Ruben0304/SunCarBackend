from pydantic import BaseModel
from typing import List

class Material(BaseModel):
    codigo: int
    descripcion: str
    um: str


class CatalogoProductos(BaseModel):
    id: str = None
    categoria: str
    materiales: List[Material]