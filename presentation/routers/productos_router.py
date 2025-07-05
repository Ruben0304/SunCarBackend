from http.client import HTTPException
from typing import List, Optional

from fastapi import APIRouter, Depends, Body
from pydantic import BaseModel

from application.services.product_service import ProductService
from infrastucture.dependencies import get_product_service
from domain.entities.producto import CatalogoProductos, Material, Cataegoria
from presentation.schemas.responses import (
    ProductoListResponse,
    CategoriaListResponse,
    MaterialListResponse,
    ProductoCreateResponse,
    CategoriaCreateResponse,
    MaterialAddResponse
)

router = APIRouter()


class ProductoCreateRequest(BaseModel):
    categoria: str
    materiales: Optional[list] = None


class MaterialAddRequest(BaseModel):
    material: dict


class CategoriaCreateRequest(BaseModel):
    categoria: str


@router.get("/", response_model=ProductoListResponse)
async def read_products(
        product_service: ProductService = Depends(get_product_service)
):
    """
    Endpoint para obtener una lista de todos los productos.
    """
    try:
        products = await product_service.get_all_products()
        return ProductoListResponse(
            success=True,
            message="Productos obtenidos exitosamente",
            data=products
        )
    except Exception as e:
        raise HTTPException()


@router.get("/categorias", response_model=CategoriaListResponse)
async def read_categories(
        product_service: ProductService = Depends(get_product_service)
):
    """
    Endpoint para obtener una lista de todas las categorías únicas de productos.
    """
    try:
        categories = await product_service.get_unique_categories()
        return CategoriaListResponse(
            success=True,
            message="Categorías obtenidas exitosamente",
            data=categories
        )
    except Exception as e:
        raise HTTPException()


@router.get("/categorias/{categoria}/materiales", response_model=MaterialListResponse)
async def read_materials_by_category(
        categoria: str,
        product_service: ProductService = Depends(get_product_service)
):
    """
    Endpoint para obtener todos los materiales únicos de una categoría específica.
    """
    try:
        materials = await product_service.get_materials_by_category(categoria)
        return MaterialListResponse(
            success=True,
            message=f"Materiales de categoría '{categoria}' obtenidos exitosamente",
            data=materials
        )
    except Exception as e:
        raise HTTPException()


@router.post("/", response_model=ProductoCreateResponse)
async def crear_producto(
    request: ProductoCreateRequest,
    product_service: ProductService = Depends(get_product_service)
):
    """
    Crear un nuevo producto (categoría) con materiales opcionales.
    """
    try:
        producto_id = await product_service.create_product(request.categoria, request.materiales)
        return ProductoCreateResponse(
            success=True,
            message="Producto creado exitosamente",
            producto_id=producto_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{producto_id}/materiales", response_model=MaterialAddResponse)
async def agregar_material_a_producto(
    producto_id: str,
    request: MaterialAddRequest,
    product_service: ProductService = Depends(get_product_service)
):
    """
    Agregar un material a un producto existente.
    """
    try:
        ok = await product_service.add_material_to_product(producto_id, request.material)
        if not ok:
            return MaterialAddResponse(
                success=False,
                message="Producto no encontrado o sin cambios"
            )
        return MaterialAddResponse(
            success=True,
            message="Material agregado exitosamente"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/categorias", response_model=CategoriaCreateResponse)
async def crear_categoria(
    request: CategoriaCreateRequest,
    product_service: ProductService = Depends(get_product_service)
):
    """
    Crear una nueva categoría (producto vacío).
    """
    try:
        categoria_id = await product_service.create_category(request.categoria)
        return CategoriaCreateResponse(
            success=True,
            message="Categoría creada exitosamente",
            categoria_id=categoria_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 