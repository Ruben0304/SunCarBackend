from typing import List, Optional
from pydantic import BaseModel
from domain.entities.producto import CatalogoProductos, Material, Cataegoria


class ProductoListResponse(BaseModel):
    success: bool
    message: str
    data: List[CatalogoProductos]


class CategoriaListResponse(BaseModel):
    success: bool
    message: str
    data: List[Cataegoria]


class MaterialListResponse(BaseModel):
    success: bool
    message: str
    data: List[Material]


class ProductoCreateResponse(BaseModel):
    success: bool
    message: str
    producto_id: str


class CategoriaCreateResponse(BaseModel):
    success: bool
    message: str
    categoria_id: str


class MaterialAddResponse(BaseModel):
    success: bool
    message: str 


class ProductoUpdateResponse(BaseModel):
    success: bool
    message: str

class ProductoDeleteResponse(BaseModel):
    success: bool
    message: str

class MaterialUpdateResponse(BaseModel):
    success: bool
    message: str

class MaterialDeleteResponse(BaseModel):
    success: bool
    message: str 