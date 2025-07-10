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
        self.collection_name = "reportes"

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

    def save_form(self, form_data: dict) -> str:
        """
        Guarda un formulario en la base de datos.
        :param form_data: Diccionario con los datos del formulario.
        :return: ID del formulario insertado.
        """
        try:
            collection = get_collection(self.collection_name)
            result = collection.insert_one(form_data)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"❌ Error guardando formulario: {e}")
            raise Exception(f"Error guardando formulario: {str(e)}")

            

    def get_reportes(self, tipo_reporte=None, cliente_numero=None, fecha_inicio=None, fecha_fin=None, lider_ci=None, descripcion=None, q=None):
        """
        Obtiene reportes con filtros opcionales y los devuelve como dicts serializables.
        Si se pasa 'q', hace búsqueda global en varios campos.
        """
        collection = get_collection(self.collection_name)
        query = {}
        if tipo_reporte:
            query["tipo_reporte"] = tipo_reporte
        if cliente_numero:
            query["cliente.numero"] = cliente_numero
        if fecha_inicio:
            query["fecha_hora.fecha"] = {"$gte": fecha_inicio}
        if fecha_fin:
            if "fecha_hora.fecha" in query:
                query["fecha_hora.fecha"]["$lte"] = fecha_fin
            else:
                query["fecha_hora.fecha"] = {"$lte": fecha_fin}
        if lider_ci:
            query["brigada.lider.CI"] = lider_ci
        if descripcion:
            query["descripcion"] = {"$regex": descripcion, "$options": "i"}
        if q:
            or_conditions = [
                {"descripcion": {"$regex": q, "$options": "i"}},
                {"cliente.nombre": {"$regex": q, "$options": "i"}},
                {"cliente.numero": {"$regex": q, "$options": "i"}},
                {"brigada.lider.nombre": {"$regex": q, "$options": "i"}},
                {"tipo_reporte": {"$regex": q, "$options": "i"}},
            ]
            query["$or"] = or_conditions
        cursor = collection.find(query)
        reportes = []
        for doc in cursor:
            doc["id"] = str(doc.pop("_id"))
            reportes.append(doc)
        return reportes

    def get_reportes_view(self, tipo_reporte=None, cliente_numero=None, fecha_inicio=None, fecha_fin=None, lider_ci=None):
        """
        Obtiene reportes desde la vista reportes_view con filtros opcionales.
        """
        collection = get_collection("reportes_view")
        query = {}
        if tipo_reporte:
            query["tipo_reporte"] = tipo_reporte
        if cliente_numero:
            query["cliente_numero"] = cliente_numero
        if fecha_inicio:
            query["fecha"] = {"$gte": fecha_inicio}
        if fecha_fin:
            if "fecha" in query:
                query["fecha"]["$lte"] = fecha_fin
            else:
                query["fecha"] = {"$lte": fecha_fin}
        if lider_ci:
            query["lider_ci"] = lider_ci
        
        cursor = collection.find(query)
        reportes = []
        for doc in cursor:
            doc["id"] = str(doc.pop("_id"))
            reportes.append(doc)
        return reportes

    def get_reporte_by_id(self, reporte_id: str) -> dict:
        """
        Obtiene un reporte por su ID.
        """
        collection = get_collection(self.collection_name)
        from bson import ObjectId
        try:
            doc = collection.find_one({"_id": ObjectId(reporte_id)})
            if not doc:
                return None
            doc["id"] = str(doc.pop("_id"))
            return doc
        except Exception as e:
            logger.error(f"❌ Error obteniendo reporte por id: {e}")
            raise Exception(f"Error obteniendo reporte por id: {str(e)}")

