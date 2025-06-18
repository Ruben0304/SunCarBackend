from pydantic import BaseModel
from typing import List


class Marca(BaseModel):
    nombre: str
    modelos: List[str]


class CatalogoProductos(BaseModel):
    id: str = None
    tipo: str
    marcas: List[Marca]
