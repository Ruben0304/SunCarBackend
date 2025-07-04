from datetime import timezone
from typing import List, Optional
from bson import ObjectId
from pydantic import ValidationError
from pymongo.errors import PyMongoError
import logging
from domain.entities.producto import CatalogoProductos, Material, Cataegoria, MaterialConFecha
from infrastucture.database.mongo_db.connection import get_collection

logger = logging.getLogger(__name__)


class ProductRepository:
    def __init__(self):
        self.collection_name = "productos"

    def get_all_products(self) -> List[CatalogoProductos]:
        try:
            collection = get_collection(self.collection_name)
            cursor = collection.find({})
            productos_raw = cursor.to_list(length=None)

            productos = []
            for producto_raw in productos_raw:
                # Transformar _id a id
                producto_raw["id"] = str(producto_raw.pop("_id"))

                # Asegurar que todos los materiales tengan 'codigo' como string
                if "materiales" in producto_raw:
                    for material in producto_raw["materiales"]:
                        if "codigo" in material:
                            material["codigo"] = str(material["codigo"])

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

    def get_unique_categories(self) -> List[Cataegoria]:
        """
        Obtiene todas las categorías únicas de productos.
        """
        try:
            collection = get_collection(self.collection_name)

            # Obtener solo los campos _id y categoria, excluyendo materiales
            cursor = collection.find({}, {"_id": 1, "categoria": 1})
            categorias_raw = cursor.to_list(length=None)

            # Transformar _id a id (igual que haces con productos)
            categorias = []
            for categoria_raw in categorias_raw:
                # Transformar _id a id
                categoria_raw["id"] = str(categoria_raw.pop("_id"))

                # Si tienes un modelo Pydantic para categorías, úsalo aquí
                categoria = Cataegoria.model_validate(categoria_raw)
                # De lo contrario, simplemente agrega el diccionario transformado
                categorias.append(categoria)

            return categorias

        except Exception as e:
            logger.error(f"❌ Error obteniendo categorías: {e}")
            raise Exception(f"Error obteniendo categorías: {str(e)}")

    def get_materials_by_category(self, categoria: str) -> List[Material]:
        """
        Obtiene todos los materiales de una categoría específica.
        """

        try:
            collection = get_collection(self.collection_name)
            categoria_object_id = ObjectId(categoria)


            # Buscar productos de la categoría específica
            cursor = collection.find({"_id": categoria_object_id}, {"_id": 0,"categoria": 0})
            productos_raw = cursor.to_list(length=None)
            materials = []


            for producto in productos_raw[0]["materiales"]:
               producto["codigo"] = str(producto["codigo"])
               material = Material.model_validate(producto)
               materials.append(material)

            return materials

        except Exception as e:
           logger.error(f"❌ Error obteniendo materiales por categoría: {e}")
           raise Exception(f"Error obteniendo materiales por categoría: {str(e)}")

    def get_last_update_date(self) -> Optional[int]:
            """
            Obtiene el timestamp (Unix) de la fecha y hora más reciente de actualización
            de todos los materiales en la colección de productos.
            """
            try:
                collection = get_collection(self.collection_name)

                pipeline = [
                    {"$unwind": "$materiales"},
                    {"$match": {"materiales.fechaAgregado": {"$exists": True}}},
                    {
                        "$group": {
                            "_id": None,
                            "ultimaActualizacion": {"$max": "$materiales.fechaAgregado"}
                        }
                    }
                ]

                result = collection.aggregate(pipeline).to_list(length=1)

                if result and len(result) > 0:
                    fecha = result[0]["ultimaActualizacion"]
                    # Asegurar que la fecha esté en UTC antes de convertir a timestamp
                    if fecha.tzinfo is None:
                        fecha = fecha.replace(tzinfo=timezone.utc)
                    return int(fecha.timestamp())
                else:
                    return None

            except Exception as e:
                raise e

    def create_category(self, categoria: str, materiales: Optional[List[dict]] = None) -> str:
        """
        Crea un nuevo producto (categoría) con materiales opcionales.
        """
        collection = get_collection(self.collection_name)
        if materiales is None:
            materiales = []
        result = collection.insert_one({
            "categoria": categoria,
            "materiales": materiales
        })
        return str(result.inserted_id)

    def add_material_to_category(self, categoria: str, material: MaterialConFecha) -> bool:
        """
        Agrega un material a todos los productos de una categoría específica.

        Args:
            categoria: Nombre de la categoría
            material: Objeto MaterialConFecha con los datos del material

        Returns:
            bool: True si se actualizó al menos un producto
        """
        try:
            collection = get_collection(self.collection_name)

            # Debug prints para ver los datos que llegan
            print(f"[DEBUG] categoria: {categoria}")
            print(f"[DEBUG] material: {material}")

            # Convertir el material a dict para MongoDB solo si es modelo Pydantic
            if hasattr(material, 'model_dump'):
                material_dict = material.model_dump()
            else:
                material_dict = material

            print(f"[DEBUG] material_dict: {material_dict}")

            # Actualizar el producto por su _id
            result = collection.update_many(
                {"_id": ObjectId(categoria)},
                {"$push": {"materiales": material_dict}}
            )

            return result.matched_count > 0

        except Exception as e:
            logger.error(f"❌ Error agregando material a la categoría: {e}")
            print(f"❌ Error agregando material a la categoría: {e}")
            raise e
