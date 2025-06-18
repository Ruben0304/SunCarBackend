from typing import List, Optional
from bson import ObjectId
from pydantic import ValidationError
from pymongo.errors import PyMongoError
import logging

from domain.entities.producto import CatalogoProductos
from infrastucture.database.mongo_db.connection import get_collection


logger = logging.getLogger(__name__)

class ProductRepository:
    def __init__(self):
        self.collection_name = "productos"

    async def get_all_products(self) -> List[CatalogoProductos]:
        try:
            collection = await get_collection(self.collection_name)
            cursor = collection.find({})
            productos_raw = await cursor.to_list(length=None)

            productos = []
            for producto_raw in productos_raw:
                # Transformar _id a id
                producto_raw["id"] = str(producto_raw.pop("_id"))

                # Usar model_validate (Pydantic v2)
                producto = CatalogoProductos.model_validate(producto_raw)
                productos.append(producto)

            return productos

        except ValidationError as e:
            logger.error(f"❌ Error de validación: {e}")
            raise Exception(f"Error de validación: {str(e)}")
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            raise Exception(f"Error: {str(e)}")

    async def get_unique_categories(self) -> List[str]:
        """
        Obtiene todas las categorías únicas de productos.
        """
        try:
            collection = await get_collection(self.collection_name)
            
            # Usar agregación para obtener categorías únicas
            pipeline = [
                {"$group": {"_id": "$categoria"}},
                {"$sort": {"_id": 1}}  # Ordenar alfabéticamente
            ]
            
            cursor = collection.aggregate(pipeline)
            categorias_raw = await cursor.to_list(length=None)
            
            # Extraer solo los nombres de las categorías
            categorias = [doc["_id"] for doc in categorias_raw]
            
            return categorias

        except Exception as e:
            logger.error(f"❌ Error obteniendo categorías: {e}")
            raise Exception(f"Error obteniendo categorías: {str(e)}")


