from typing import List, Optional
from bson import ObjectId
from pydantic import ValidationError
from pymongo.errors import PyMongoError
import logging

from domain.entities.form import Form
from infrastucture.database.mongo_db.connection import get_collection

logger = logging.getLogger(__name__)


class FormRepository:
    def __init__(self):
        self.collection_name = "forms"

    def get_all_forms(self) -> List[Form]:
        try:
            collection = get_collection(self.collection_name)
            cursor = collection.find({})
            formularios_raw = cursor.to_list(length=None)

            formularios = []
            for formulario_raw in formularios_raw:
                # Transformar _id a id
                formulario_raw["id"] = str(formulario_raw.pop("_id"))

                # Usar model_validate (Pydantic v2)
                formulario = Form.model_validate(formulario_raw)
                formularios.append(formulario)

            return formularios

        except ValidationError as e:
            logger.error(f"❌ Error de validación: {e}")
            raise Exception(f"Error de validación: {str(e)}")
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            raise Exception(f"Error: {str(e)}")

    def get_forms_by_service_type(self, service_type: str) -> List[Form]:
        """
        Obtiene todos los formularios de un tipo de servicio específico.
        """
        try:
            collection = get_collection(self.collection_name)
            cursor = collection.find({"service_type": service_type})
            formularios_raw = cursor.to_list(length=None)

            formularios = []
            for formulario_raw in formularios_raw:
                # Transformar _id a id
                formulario_raw["id"] = str(formulario_raw.pop("_id"))

                # Usar model_validate (Pydantic v2)
                formulario = Form.model_validate(formulario_raw)
                formularios.append(formulario)

            return formularios

        except ValidationError as e:
            logger.error(f"❌ Error de validación: {e}")
            raise Exception(f"Error de validación: {str(e)}")
        except Exception as e:
            logger.error(f"❌ Error obteniendo formularios por tipo de servicio: {e}")
            raise Exception(f"Error obteniendo formularios por tipo de servicio: {str(e)}")

    def get_forms_by_brigade_chief(self, brigade_chief: str) -> List[Form]:
        """
        Obtiene todos los formularios de un jefe de brigada específico.
        """
        try:
            collection = get_collection(self.collection_name)
            cursor = collection.find({"brigade_chief": brigade_chief})
            formularios_raw = cursor.to_list(length=None)

            formularios = []
            for formulario_raw in formularios_raw:
                # Transformar _id a id
                formulario_raw["id"] = str(formulario_raw.pop("_id"))

                # Usar model_validate (Pydantic v2)
                formulario = Form.model_validate(formulario_raw)
                formularios.append(formulario)

            return formularios

        except ValidationError as e:
            logger.error(f"❌ Error de validación: {e}")
            raise Exception(f"Error de validación: {str(e)}")
        except Exception as e:
            logger.error(f"❌ Error obteniendo formularios por jefe de brigada: {e}")
            raise Exception(f"Error obteniendo formularios por jefe de brigada: {str(e)}")
