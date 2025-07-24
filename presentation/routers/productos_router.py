from typing import List, Optional

from fastapi import APIRouter, Depends, Body, Path, HTTPException
from pydantic import BaseModel

from application.services.product_service import ProductService
from infrastucture.dependencies import get_product_service
from domain.entities.producto import CatalogoProductos, Material, Cataegoria
from presentation.schemas.responses.productos_responses import (
    ProductoListResponse,
    CategoriaListResponse,
    MaterialListResponse,
    ProductoCreateResponse,
    CategoriaCreateResponse,
    MaterialAddResponse,
    ProductoUpdateResponse,
    ProductoDeleteResponse,
    MaterialUpdateResponse,
    MaterialDeleteResponse
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
        raise HTTPException(status_code=500, detail=str(e))


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
        raise HTTPException(status_code=500, detail=str(e))


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
        raise HTTPException(status_code=500, detail=str(e))


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


@router.delete("/{producto_id}", response_model=ProductoDeleteResponse)
async def eliminar_producto(
    producto_id: str = Path(..., description="ID del producto a eliminar"),
    product_service: ProductService = Depends(get_product_service)
):
    """
    Eliminar un producto completo por su id.
    """
    try:
        ok = await product_service.delete_product(producto_id)
        if not ok:
            return ProductoDeleteResponse(success=False, message="Producto no encontrado o no eliminado")
        return ProductoDeleteResponse(success=True, message="Producto eliminado exitosamente")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{producto_id}", response_model=ProductoUpdateResponse)
async def editar_producto(
    producto_id: str,
    new_data: dict = Body(..., description="Nuevos datos del producto (categoria, materiales, etc.)"),
    product_service: ProductService = Depends(get_product_service)
):
    """
    Editar todos los atributos de un producto (incluyendo categoría y materiales).
    """
    try:
        ok = await product_service.update_product(producto_id, new_data)
        if not ok:
            return ProductoUpdateResponse(success=False, message="Producto no encontrado o sin cambios")
        return ProductoUpdateResponse(success=True, message="Producto actualizado exitosamente")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{producto_id}/materiales/{material_codigo}", response_model=MaterialDeleteResponse)
async def eliminar_material(
    producto_id: str,
    material_codigo: str,
    product_service: ProductService = Depends(get_product_service)
):
    """
    Eliminar un material de un producto por su código.
    """
    try:
        ok = await product_service.delete_material_from_product(producto_id, material_codigo)
        if not ok:
            return MaterialDeleteResponse(success=False, message="Material no encontrado o no eliminado")
        return MaterialDeleteResponse(success=True, message="Material eliminado exitosamente")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{producto_id}/materiales/{material_codigo}", response_model=MaterialUpdateResponse)
async def editar_material(
    producto_id: str,
    material_codigo: str,
    new_material: dict = Body(..., description="Nuevos datos del material (codigo, descripcion, um)"),
    product_service: ProductService = Depends(get_product_service)
):
    """
    Editar todos los atributos de un material dentro de un producto.
    """
    try:
        ok = await product_service.update_material_in_product(producto_id, material_codigo, new_material)
        if not ok:
            return MaterialUpdateResponse(success=False, message="Material no encontrado o sin cambios")
        return MaterialUpdateResponse(success=True, message="Material actualizado exitosamente")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 