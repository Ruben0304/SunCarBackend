from typing import List
from fastapi import Depends


from infrastucture.repositories.productos_repository import ProductRepository
from domain.entities.producto import CatalogoProductos, Material

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

    async def get_materials_by_category(self, categoria: str) -> List[Material]:
        """
        Obtiene todos los materiales únicos de una categoría específica.
        """
        return await self.productos_repository.get_materials_by_category(categoria)

