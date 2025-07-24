from typing import List, Optional
from fastapi import Depends


from infrastucture.repositories.productos_repository import ProductRepository
from domain.entities.producto import CatalogoProductos, Material, Cataegoria


class ProductService:
    def __init__(self, productos_repository: ProductRepository):
        self.productos_repository = productos_repository

    async def get_all_products(self) -> List[CatalogoProductos]:
        """
        Obtiene todos los productos del catálogo.
        """
        return  self.productos_repository.get_all_products()

    async def get_unique_categories(self) -> List[Cataegoria]:
        """
        Obtiene todas las categorías únicas de productos.
        """
        return  self.productos_repository.get_unique_categories()

    async def get_materials_by_category(self, categoria: str) -> List[Material]:
        """
        Obtiene todos los materiales únicos de una categoría específica.
        """
        return  self.productos_repository.get_materials_by_category(categoria)

    async def create_product(self, categoria: str, materiales: Optional[list] = None) -> str:
        """
        Crea un nuevo producto (categoría) con materiales opcionales.
        """
        return self.productos_repository.create_category(categoria, materiales)

    async def add_material_to_product(self, producto_id: str, material: dict) -> bool:
        """
        Agrega un material a un producto existente.
        """
        from domain.entities.producto import MaterialConFecha
        if not isinstance(material, MaterialConFecha):
            material = MaterialConFecha(**material)
        return self.productos_repository.add_material_to_category(producto_id, material)

    async def create_category(self, categoria: str) -> str:
        """
        Crea una nueva categoría (producto vacío).
        """
        return self.productos_repository.create_category(categoria, materiales=[])

    async def delete_material_from_product(self, producto_id: str, material_codigo: str) -> bool:
        """
        Elimina un material de un producto por su código.
        """
        return self.productos_repository.delete_material_from_product(producto_id, material_codigo)

    async def update_material_in_product(self, producto_id: str, material_codigo: str, new_material: dict) -> bool:
        """
        Edita todos los atributos de un material dentro de un producto.
        """
        return self.productos_repository.update_material_in_product(producto_id, material_codigo, new_material)

    async def update_product(self, producto_id: str, new_data: dict) -> bool:
        """
        Edita todos los atributos de un producto (incluyendo categoría y materiales).
        """
        return self.productos_repository.update_product(producto_id, new_data)

    async def delete_product(self, producto_id: str) -> bool:
        """
        Elimina un producto completo por su id.
        """
        return self.productos_repository.delete_product(producto_id)

