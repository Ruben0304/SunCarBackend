from http.client import HTTPException
from typing import List

from fastapi import APIRouter, Depends

from application.services.product_service import ProductService
from application.services.worker_service import WorkerService
from domain.entities.producto import CatalogoProductos, Material
from domain.entities.trabajador import Trabajador
from infrastucture.dependencies import get_product_service, get_worker_service

router = APIRouter()


@router.get("/productos_por_tipo_y_marca", response_model=List[CatalogoProductos])
async def read_products(
        product_service: ProductService = Depends(get_product_service)
):
    """
    Endpoint para obtener una lista de todos los productos.
    """
    try:
        products = await product_service.get_all_products()
        return products
    except Exception as e:
        raise HTTPException()


@router.get("/categorias", response_model=List[str])
async def read_categories(
        product_service: ProductService = Depends(get_product_service)
):
    """
    Endpoint para obtener una lista de todas las categorías únicas de productos.
    """
    try:
        categories = await product_service.get_unique_categories()
        return categories
    except Exception as e:
        raise HTTPException()


@router.get("/categorias/{categoria}/materiales", response_model=List[Material])
async def read_materials_by_category(
        categoria: str,
        product_service: ProductService = Depends(get_product_service)
):
    """
    Endpoint para obtener todos los materiales únicos de una categoría específica.
    """
    try:
        materials = await product_service.get_materials_by_category(categoria)
        return materials
    except Exception as e:
        raise HTTPException()


@router.get("/trabajadores", response_model=List[Trabajador])
async def read_workers(
        worker_service: WorkerService = Depends(get_worker_service)
):
    """
    Endpoint to get a list of all workers.
    """
    try:
        workers = await worker_service.get_all_workers()
        return workers
    except Exception as e:
        raise HTTPException()