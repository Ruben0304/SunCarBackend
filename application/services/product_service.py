from typing import List

from fastapi import Depends

from infrastucture.dependencies import get_productos_repository
from infrastucture.repositories.productos_repository import ProductRepository
from domain.entities.producto import CatalogoProductos

class ProductService:
    def __init__(self, productos_repository: ProductRepository):
        self.productos_repository = productos_repository

    async def get_all_products(self) -> List[CatalogoProductos]:
        """
        Obtiene todos los productos del catálogo.
        """
        return await self.productos_repository.get_all_products()

# Función para obtener la instancia del servicio (dependency injection para FastAPI)
def get_product_service(
        productos_repository: ProductRepository = Depends(get_productos_repository)
) -> ProductService:
    """
    Dependency para FastAPI que devuelve la instancia del ProductService.
    """
    return ProductService(productos_repository)