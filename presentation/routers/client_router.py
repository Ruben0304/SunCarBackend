from http.client import HTTPException
from typing import List

from fastapi import APIRouter, Depends


from application.services.product_service import get_product_service
from application.services.worker_service import WorkerService, get_worker_service
from domain.entities.producto import CatalogoProductos
from domain.entities.trabajador import Trabajador

router = APIRouter()


class ProductService:
    async def get_all_products(self):
        pass


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