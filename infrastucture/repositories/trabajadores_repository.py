from typing import List, Optional
from bson import ObjectId
from pydantic import ValidationError
from pymongo.errors import PyMongoError
import logging

from domain.entities.trabajador import Trabajador
from infrastucture.database.mongo_db.connection import get_collection

logger = logging.getLogger(__name__)


class WorkerRepository:
    def __init__(self):
        self.collection_name = "trabajadores"

    def get_all_workers(self) -> List[Trabajador]:
        try:
            collection = get_collection(self.collection_name)
            cursor = collection.find({})
            workers_raw = cursor.to_list(length=None)

            workers = []
            for worker_raw in workers_raw:
                # Transformar _id a id
                worker_raw["id"] = str(worker_raw.pop("_id"))

                # Usar model_validate (Pydantic v2)
                worker = Trabajador.model_validate(worker_raw)
                workers.append(worker)

            return workers

        except ValidationError as e:
            logger.error(f"❌ Error de validación: {e}")
            raise Exception(f"Error de validación: {str(e)}")
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            raise Exception(f"Error: {str(e)}")

    def login(self, ci: str, contraseña: str) -> bool:
        """
        Autentica un trabajador usando su CI y contraseña.
        
        Args:
            ci: Cédula de identidad del trabajador
            contraseña: Contraseña del trabajador
            
        Returns:
            bool: True si las credenciales son correctas, False en caso contrario
        """
        try:
            collection = get_collection(self.collection_name)
            
            # Buscar el trabajador por CI
            worker_raw = collection.find_one({"CI": ci})
            
            if worker_raw is None:
                logger.warning(f"⚠️ Trabajador con CI {ci} no encontrado")
                return False
            
            # Verificar si el trabajador tiene contraseña
            if "contraseña" not in worker_raw:
                logger.warning(f"⚠️ Trabajador con CI {ci} no tiene contraseña configurada")
                return False
            
            # Verificar si la contraseña coincide
            if worker_raw["contraseña"] == contraseña:
                logger.info(f"✅ Login exitoso para trabajador con CI {ci}")
                return True
            else:
                logger.warning(f"⚠️ Contraseña incorrecta para trabajador con CI {ci}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error durante el login: {e}")
            raise Exception(f"Error durante el login: {str(e)}")

    def create_worker(self, ci: str, nombre: str, contrasena: str = None) -> str:
        collection = get_collection(self.collection_name)
        data = {"CI": ci, "nombre": nombre}
        if contrasena:
            data["contraseña"] = contrasena
        result = collection.insert_one(data)
        return str(result.inserted_id)

    def search_workers_by_name(self, nombre: str) -> list:
        collection = get_collection(self.collection_name)
        cursor = collection.find({"nombre": {"$regex": nombre, "$options": "i"}})
        workers_raw = cursor.to_list(length=None)
        workers = []
        for worker_raw in workers_raw:
            worker_raw["id"] = str(worker_raw.pop("_id"))
            worker = Trabajador.model_validate(worker_raw)
            workers.append(worker)
        return workers

    def set_worker_password(self, ci: str, contrasena: str) -> bool:
        collection = get_collection(self.collection_name)
        result = collection.update_one({"CI": ci}, {"$set": {"contraseña": contrasena}})
        return result.modified_count > 0
