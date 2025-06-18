from typing import List

from fastapi import Depends


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

    async def get_unique_categories(self) -> List[str]:
        """
        Obtiene todas las categorías únicas de productos.
        """
        return await self.productos_repository.get_unique_categories()

