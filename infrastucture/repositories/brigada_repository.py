from typing import List, Optional
from bson import ObjectId
from pydantic import ValidationError
from pymongo.errors import PyMongoError
import logging
from bson.errors import InvalidId

from domain.entities.brigada import Brigada
from domain.entities.trabajador import Trabajador
from infrastucture.database.mongo_db.connection import get_collection

logger = logging.getLogger(__name__)


class BrigadaRepository:
    def __init__(self):
        self.collection_name = "brigadas_completas"  # Ahora apunta a la view

    def get_brigada_by_lider_ci(self, lider_ci: str) -> Optional[Brigada]:
        """
        Obtiene una brigada completa usando la view brigadas_completas.
        Esta es la forma más eficiente ya que la view ya tiene todos los datos unidos.
        
        Args:
            lider_ci: Cédula de identidad del líder de la brigada
            
        Returns:
            Brigada: Objeto brigada con datos completos de líder e integrantes, o None si no se encuentra
        """
        try:
            collection = get_collection(self.collection_name)
            
            # Buscar en la view usando el campo lider_ci
            brigada_raw = collection.find_one({"lider_ci": lider_ci})
            
            if brigada_raw is None:
                logger.warning(f"⚠️ Brigada con líder CI {lider_ci} no encontrada")
                return None
            
            # Verificar que se encontró el líder
            if not brigada_raw.get("lider"):
                logger.error(f"❌ Líder con CI {lider_ci} no encontrado en la view")
                raise Exception(f"Líder con CI {lider_ci} no encontrado")
            
            # Transformar _id a id para el líder
            lider_raw = brigada_raw["lider"]
            lider_raw["id"] = str(lider_raw.pop("_id"))
            lider_raw["tiene_contraseña"] = bool(lider_raw.get("contraseña"))
            lider = Trabajador.model_validate(lider_raw)
            
            # Transformar _id a id para todos los integrantes
            integrantes = []
            for integrante_raw in brigada_raw.get("integrantes", []):
                integrante_raw["id"] = str(integrante_raw.pop("_id"))
                integrante_raw["tiene_contraseña"] = self._get_tiene_contraseña(integrante_raw["CI"])
                integrante = Trabajador.model_validate(integrante_raw)
                integrantes.append(integrante)
            
            # Crear y retornar la brigada completa
            brigada = Brigada(
                id=str(brigada_raw["_id"]) if "_id" in brigada_raw else brigada_raw.get("lider_ci"),
                lider_ci=brigada_raw["lider_ci"],
                lider=lider, 
                integrantes=integrantes
            )
            
            logger.info(f"✅ Brigada obtenida exitosamente (view) para líder CI {lider_ci} con {len(integrantes)} integrantes")
            return brigada
            
        except ValidationError as e:
            logger.error(f"❌ Error de validación: {e}")
            raise Exception(f"Error de validación: {str(e)}")
        except Exception as e:
            logger.error(f"❌ Error obteniendo brigada desde view: {e}")
            raise Exception(f"Error obteniendo brigada desde view: {str(e)}")

    def get_all_brigadas(self) -> List[Brigada]:
        """
        Obtiene todas las brigadas completas usando la view.
        
        Returns:
            List[Brigada]: Lista de todas las brigadas con datos completos
        """
        try:
            collection = get_collection(self.collection_name)
            
            # Obtener todas las brigadas de la view
            cursor = collection.find({})
            brigadas_raw = cursor.to_list(length=None)
            
            brigadas = []
            for brigada_raw in brigadas_raw:
                # Verificar que se encontró el líder
                if not brigada_raw.get("lider"):
                    logger.warning(f"⚠️ Brigada sin líder encontrada, saltando...")
                    continue
                
                # Transformar _id a id para el líder
                lider_raw = brigada_raw["lider"]
                lider_raw["id"] = str(lider_raw.pop("_id"))
                lider_raw["tiene_contraseña"] = bool(lider_raw.get("contraseña"))
                lider = Trabajador.model_validate(lider_raw)
                
                # Transformar _id a id para todos los integrantes
                integrantes = []
                for integrante_raw in brigada_raw.get("integrantes", []):
                    integrante_raw["id"] = str(integrante_raw.pop("_id"))
                    integrante_raw["tiene_contraseña"] = self._get_tiene_contraseña(integrante_raw["CI"])
                    integrante = Trabajador.model_validate(integrante_raw)
                    integrantes.append(integrante)
                
                # Crear la brigada
                brigada = Brigada(
                    id=str(brigada_raw["_id"]) if "_id" in brigada_raw else brigada_raw.get("lider_ci"),
                    lider_ci=brigada_raw["lider_ci"],
                    lider=lider, 
                    integrantes=integrantes
                )
                brigadas.append(brigada)
            
            logger.info(f"✅ {len(brigadas)} brigadas obtenidas exitosamente desde la view")
            return brigadas
            
        except ValidationError as e:
            logger.error(f"❌ Error de validación: {e}")
            raise Exception(f"Error de validación: {str(e)}")
        except Exception as e:
            logger.error(f"❌ Error obteniendo todas las brigadas desde view: {e}")
            raise Exception(f"Error obteniendo todas las brigadas desde view: {str(e)}")

    def get_brigadas_by_integrante_ci(self, integrante_ci: str) -> List[Brigada]:
        """
        Obtiene todas las brigadas donde un trabajador específico es integrante.
        
        Args:
            integrante_ci: Cédula de identidad del integrante
            
        Returns:
            List[Brigada]: Lista de brigadas donde el trabajador es integrante
        """
        try:
            collection = get_collection(self.collection_name)
            
            # Buscar brigadas donde el CI esté en la lista de integrantes
            cursor = collection.find({"integrantes.CI": integrante_ci})
            brigadas_raw = cursor.to_list(length=None)
            
            brigadas = []
            for brigada_raw in brigadas_raw:
                # Verificar que se encontró el líder
                if not brigada_raw.get("lider"):
                    logger.warning(f"⚠️ Brigada sin líder encontrada, saltando...")
                    continue
                
                # Transformar _id a id para el líder
                lider_raw = brigada_raw["lider"]
                lider_raw["id"] = str(lider_raw.pop("_id"))
                lider_raw["tiene_contraseña"] = bool(lider_raw.get("contraseña"))
                lider = Trabajador.model_validate(lider_raw)
                
                # Transformar _id a id para todos los integrantes
                integrantes = []
                for integrante_raw in brigada_raw.get("integrantes", []):
                    integrante_raw["id"] = str(integrante_raw.pop("_id"))
                    integrante_raw["tiene_contraseña"] = self._get_tiene_contraseña(integrante_raw["CI"])
                    integrante = Trabajador.model_validate(integrante_raw)
                    integrantes.append(integrante)
                
                # Crear la brigada
                brigada = Brigada(
                    id=str(brigada_raw["_id"]) if "_id" in brigada_raw else brigada_raw.get("lider_ci"),
                    lider_ci=brigada_raw["lider_ci"],
                    lider=lider, 
                    integrantes=integrantes
                )
                brigadas.append(brigada)
            
            logger.info(f"✅ {len(brigadas)} brigadas encontradas para integrante CI {integrante_ci}")
            return brigadas
            
        except ValidationError as e:
            logger.error(f"❌ Error de validación: {e}")
            raise Exception(f"Error de validación: {str(e)}")
        except Exception as e:
            logger.error(f"❌ Error obteniendo brigadas por integrante: {e}")
            raise Exception(f"Error obteniendo brigadas por integrante: {str(e)}")

    def create_brigada(self, lider_ci: str, integrantes_ci: List[str]) -> str:
        """
        Crea una nueva brigada en la colección base (no la view).
        Retorna el id de la brigada creada.
        """
        collection = get_collection("brigadas")
        result = collection.insert_one({
            "lider": lider_ci,
            "integrantes": integrantes_ci
        })
        return str(result.inserted_id)

    def update_brigada(self, brigada_id: str, lider_ci: str, integrantes_ci: List[str]) -> bool:
        """
        Actualiza una brigada existente en la colección base.
        """
        collection = get_collection("brigadas")
        result = collection.update_one({"_id": ObjectId(brigada_id)}, {"$set": {"lider": lider_ci, "integrantes": integrantes_ci}})
        return result.modified_count > 0

    def delete_brigada(self, brigada_id: str) -> bool:
        """
        Elimina una brigada por su id en la colección base.
        """
        collection = get_collection("brigadas")
        result = collection.delete_one({"_id": ObjectId(brigada_id)})
        return result.deleted_count > 0

    def delete_brigada_by_lider_ci(self, lider_ci: str) -> bool:
        """
        Elimina una brigada por el CI del líder en la colección base.
        """
        collection = get_collection("brigadas")
        result = collection.delete_one({"lider": lider_ci})
        return result.deleted_count > 0

    def add_trabajador(self, brigada_id: str, trabajador_ci: str) -> bool:
        """
        Agrega un trabajador a la lista de integrantes de una brigada.
        """
        collection = get_collection("brigadas")
        # Intentar usar como ObjectId
        try:
            obj_id = ObjectId(brigada_id)
            result = collection.update_one({"_id": obj_id}, {"$addToSet": {"integrantes": trabajador_ci}})
            if result.modified_count > 0:
                return True
        except (InvalidId, TypeError):
            pass
        # Si no es ObjectId válido, buscar por lider_ci
        result = collection.update_one({"lider": brigada_id}, {"$addToSet": {"integrantes": trabajador_ci}})
        return result.modified_count > 0

    def remove_trabajador(self, brigada_id: str, trabajador_ci: str) -> bool:
        """
        Elimina un trabajador de la lista de integrantes de una brigada.
        """
        collection = get_collection("brigadas")
        result = collection.update_one({"_id": ObjectId(brigada_id)}, {"$pull": {"integrantes": trabajador_ci}})
        return result.modified_count > 0

    def remove_trabajador_by_lider_ci(self, lider_ci: str, trabajador_ci: str) -> bool:
        """
        Elimina un trabajador de la lista de integrantes de una brigada usando el CI del líder.
        """
        collection = get_collection("brigadas")
        result = collection.update_one({"lider": lider_ci}, {"$pull": {"integrantes": trabajador_ci}})
        return result.modified_count > 0

    def update_trabajador(self, trabajador_ci: str, nombre: str) -> bool:
        """
        Actualiza los datos de un trabajador (solo nombre por simplicidad).
        """
        collection = get_collection("trabajadores")
        result = collection.update_one({"CI": trabajador_ci}, {"$set": {"nombre": nombre}})
        return result.modified_count > 0

    def _get_tiene_contraseña(self, ci: str) -> bool:
        collection = get_collection("trabajadores")
        worker = collection.find_one({"CI": ci})
        return bool(worker and worker.get("contraseña"))
