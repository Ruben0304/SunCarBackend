from datetime import datetime, timezone
from typing import List, Optional
from bson import ObjectId
from pydantic import ValidationError
import logging
from domain.entities.update import AppVersionConfig
from infrastucture.database.mongo_db.connection import get_collection

logger = logging.getLogger(__name__)


class UpdateRepository:
    def __init__(self):
        self.collection_name = "app_updates"

    def get_app_version_config(self, platform: str) -> Optional[AppVersionConfig]:
        """
        Obtiene la configuración de versión de app para una plataforma específica
        """
        try:
            collection = get_collection(self.collection_name)
            config_raw = collection.find_one({"platform": platform.lower()})
            
            if not config_raw:
                return None
            
            # Transformar _id a id
            config_raw["id"] = str(config_raw.pop("_id"))
            
            return AppVersionConfig.model_validate(config_raw)
            
        except ValidationError as e:
            logger.error(f"❌ Error de validación: {e}")
            raise Exception(f"Error de validación: {str(e)}")
        except Exception as e:
            logger.error(f"❌ Error obteniendo configuración de app: {e}")
            raise Exception(f"Error obteniendo configuración de app: {str(e)}")

    def get_all_app_version_configs(self) -> List[AppVersionConfig]:
        """
        Obtiene todas las configuraciones de versiones de app
        """
        try:
            collection = get_collection(self.collection_name)
            cursor = collection.find({})
            configs_raw = cursor.to_list(length=None)
            
            configs = []
            for config_raw in configs_raw:
                # Transformar _id a id
                config_raw["id"] = str(config_raw.pop("_id"))
                config = AppVersionConfig.model_validate(config_raw)
                configs.append(config)
            
            return configs
            
        except ValidationError as e:
            logger.error(f"❌ Error de validación: {e}")
            raise Exception(f"Error de validación: {str(e)}")
        except Exception as e:
            logger.error(f"❌ Error obteniendo configuraciones: {e}")
            raise Exception(f"Error obteniendo configuraciones: {str(e)}")

    def create_app_version_config(self, config: AppVersionConfig) -> str:
        """
        Crea una nueva configuración de versión de app
        """
        try:
            collection = get_collection(self.collection_name)
            
            # Preparar datos para inserción
            config_dict = config.model_dump(exclude={"id"})
            config_dict["created_at"] = datetime.now(timezone.utc)
            config_dict["updated_at"] = datetime.now(timezone.utc)
            
            result = collection.insert_one(config_dict)
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"❌ Error creando configuración: {e}")
            raise Exception(f"Error creando configuración: {str(e)}")

    def update_app_version_config(self, platform: str, config: AppVersionConfig) -> bool:
        """
        Actualiza la configuración de versión de app para una plataforma
        """
        try:
            collection = get_collection(self.collection_name)
            
            # Preparar datos para actualización
            config_dict = config.model_dump(exclude={"id", "created_at"})
            config_dict["updated_at"] = datetime.now(timezone.utc)
            
            result = collection.update_one(
                {"platform": platform.lower()},
                {"$set": config_dict}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"❌ Error actualizando configuración: {e}")
            raise Exception(f"Error actualizando configuración: {str(e)}")

    def delete_app_version_config(self, platform: str) -> bool:
        """
        Elimina la configuración de versión de app para una plataforma
        """
        try:
            collection = get_collection(self.collection_name)
            result = collection.delete_one({"platform": platform.lower()})
            return result.deleted_count > 0
            
        except Exception as e:
            logger.error(f"❌ Error eliminando configuración: {e}")
            raise Exception(f"Error eliminando configuración: {str(e)}")

    def upsert_app_version_config(self, config: AppVersionConfig) -> str:
        """
        Crea o actualiza una configuración de versión de app (upsert)
        """
        try:
            collection = get_collection(self.collection_name)
            
            # Preparar datos
            config_dict = config.model_dump(exclude={"id"})
            current_time = datetime.now(timezone.utc)
            
            # Para upsert, establecemos created_at solo si es nuevo
            update_data = {
                "$set": {**config_dict, "updated_at": current_time},
                "$setOnInsert": {"created_at": current_time}
            }
            
            result = collection.update_one(
                {"platform": config.platform.lower()},
                update_data,
                upsert=True
            )
            
            if result.upserted_id:
                return str(result.upserted_id)
            else:
                # Si fue una actualización, obtenemos el ID existente
                existing = collection.find_one({"platform": config.platform.lower()})
                return str(existing["_id"]) if existing else ""
                
        except Exception as e:
            logger.error(f"❌ Error en upsert de configuración: {e}")
            raise Exception(f"Error en upsert de configuración: {str(e)}")