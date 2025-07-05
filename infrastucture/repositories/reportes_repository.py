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

    def get_hours_worked_by_ci(self, ci: str, fecha_inicio: str, fecha_fin: str) -> float:
        """
        Obtiene el total de horas trabajadas por una persona dado su CI y rango de fechas.
        
        :param ci: Cédula de identidad de la persona
        :param fecha_inicio: Fecha de inicio del rango (formato: YYYY-MM-DD)
        :param fecha_fin: Fecha de fin del rango (formato: YYYY-MM-DD)
        :return: Total de horas trabajadas
        """
        try:
            collection = get_collection(self.collection_name)

            pipeline = [
                {
                    "$match": {
                        "$and": [
                            {
                                "fecha_hora.fecha": {
                                    "$gte": fecha_inicio,
                                    "$lte": fecha_fin
                                }
                            },
                            {
                                "$or": [
                                    {"brigada.lider.CI": ci},
                                    {"brigada.integrantes.CI": ci}
                                ]
                            }
                        ]
                    }
                },
                {
                    "$addFields": {
                        "horas_trabajadas": {
                            "$divide": [
                                {
                                    "$subtract": [
                                        {
                                            "$add": [
                                                {
                                                    "$multiply": [
                                                        {"$toInt": {"$substr": ["$fecha_hora.hora_fin", 0, 2]}},
                                                        60
                                                    ]
                                                },
                                                {"$toInt": {"$substr": ["$fecha_hora.hora_fin", 3, 2]}}
                                            ]
                                        },
                                        {
                                            "$add": [
                                                {
                                                    "$multiply": [
                                                        {"$toInt": {"$substr": ["$fecha_hora.hora_inicio", 0, 2]}},
                                                        60
                                                    ]
                                                },
                                                {"$toInt": {"$substr": ["$fecha_hora.hora_inicio", 3, 2]}}
                                            ]
                                        }
                                    ]
                                },
                                60
                            ]
                        }
                    }
                },
                {
                    "$group": {
                        "_id": None,
                        "total_horas": {"$sum": "$horas_trabajadas"}
                    }
                }
            ]

            result = list(collection.aggregate(pipeline))

            if result:
                return round(result[0]["total_horas"], 2)
            else:
                return 0.0

        except Exception as e:
            logger.error(f"❌ Error obteniendo horas trabajadas por CI: {e}")
            raise Exception(f"Error obteniendo horas trabajadas por CI: {str(e)}")

    def get_all_workers_hours_worked(self, fecha_inicio: str, fecha_fin: str) -> List[dict]:
        """
        Obtiene todos los trabajadores con sus horas trabajadas en un rango de fechas específico.
        
        :param fecha_inicio: Fecha de inicio del rango (formato: YYYY-MM-DD)
        :param fecha_fin: Fecha de fin del rango (formato: YYYY-MM-DD)
        :return: Lista de trabajadores con sus horas trabajadas
        """
        try:
            collection = get_collection(self.collection_name)

            pipeline = [
                {
                    "$match": {
                        "fecha_hora.fecha": {
                            "$gte": fecha_inicio,
                            "$lte": fecha_fin
                        }
                    }
                },
                {
                    "$addFields": {
                        "horas_trabajadas": {
                            "$divide": [
                                {
                                    "$subtract": [
                                        {
                                            "$add": [
                                                {
                                                    "$multiply": [
                                                        {"$toInt": {"$substr": ["$fecha_hora.hora_fin", 0, 2]}},
                                                        60
                                                    ]
                                                },
                                                {"$toInt": {"$substr": ["$fecha_hora.hora_fin", 3, 2]}}
                                            ]
                                        },
                                        {
                                            "$add": [
                                                {
                                                    "$multiply": [
                                                        {"$toInt": {"$substr": ["$fecha_hora.hora_inicio", 0, 2]}},
                                                        60
                                                    ]
                                                },
                                                {"$toInt": {"$substr": ["$fecha_hora.hora_inicio", 3, 2]}}
                                            ]
                                        }
                                    ]
                                },
                                60
                            ]
                        }
                    }
                },
                {
                    "$project": {
                        "horas_trabajadas": 1,
                        "lider": "$brigada.lider",
                        "integrantes": "$brigada.integrantes"
                    }
                },
                {
                    "$facet": {
                        "lideres": [
                            {
                                "$unwind": "$lider"
                            },
                            {
                                "$group": {
                                    "_id": "$lider.CI",
                                    "nombre": {"$first": "$lider.nombre"},
                                    "apellido": {"$first": "$lider.apellido"},
                                    "total_horas": {"$sum": "$horas_trabajadas"}
                                }
                            }
                        ],
                        "integrantes": [
                            {
                                "$unwind": "$integrantes"
                            },
                            {
                                "$group": {
                                    "_id": "$integrantes.CI",
                                    "nombre": {"$first": "$integrantes.nombre"},
                                    "apellido": {"$first": "$integrantes.apellido"},
                                    "total_horas": {"$sum": "$horas_trabajadas"}
                                }
                            }
                        ]
                    }
                },
                {
                    "$project": {
                        "todos_trabajadores": {
                            "$concatArrays": ["$lideres", "$integrantes"]
                        }
                    }
                },
                {
                    "$unwind": "$todos_trabajadores"
                },
                {
                    "$group": {
                        "_id": "$todos_trabajadores._id",
                        "nombre": {"$first": "$todos_trabajadores.nombre"},
                        "apellido": {"$first": "$todos_trabajadores.apellido"},
                        "total_horas": {"$sum": "$todos_trabajadores.total_horas"}
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "ci": "$_id",
                        "nombre": 1,
                        "apellido": 1,
                        "total_horas": {"$round": ["$total_horas", 2]}
                    }
                },
                {
                    "$sort": {"total_horas": -1}
                }
            ]

            result = list(collection.aggregate(pipeline))
            return result

        except Exception as e:
            logger.error(f"❌ Error obteniendo horas trabajadas de todos los trabajadores: {e}")
            raise Exception(f"Error obteniendo horas trabajadas de todos los trabajadores: {str(e)}")

  
