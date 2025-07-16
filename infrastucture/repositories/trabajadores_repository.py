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
        self.reportes_collection_name = "reportes"

    def get_all_workers(self) -> List[Trabajador]:
        try:
            collection = get_collection(self.collection_name)
            cursor = collection.find({})
            workers_raw = cursor.to_list(length=None)

            workers = []
            for worker_raw in workers_raw:
                # Transformar _id a id
                worker_raw["id"] = str(worker_raw.pop("_id"))
                # Determinar si tiene contraseña
                worker_raw["tiene_contraseña"] = bool(worker_raw.get("contraseña"))
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

    def get_hours_worked_by_ci(self, ci: str, fecha_inicio: str, fecha_fin: str) -> float:
        """
        Obtiene el total de horas trabajadas por una persona dado su CI y rango de fechas.
        
        :param ci: Cédula de identidad de la persona
        :param fecha_inicio: Fecha de inicio del rango (formato: YYYY-MM-DD)
        :param fecha_fin: Fecha de fin del rango (formato: YYYY-MM-DD)
        :return: Total de horas trabajadas
        """
        try:
            collection = get_collection(self.reportes_collection_name)

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
            collection = get_collection(self.reportes_collection_name)

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
                        "total_horas": {"$sum": "$todos_trabajadores.total_horas"}
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "ci": "$_id",
                        "nombre": 1,
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

    async def convert_worker_to_leader(self, ci: str, contrasena: str = None, integrantes: list = None) -> bool:
        """
        Convierte un trabajador existente en jefe de brigada:
        - Si no tiene contraseña, se la asigna.
        - Si se pasan integrantes, crea/actualiza la brigada con este trabajador como líder.
        """
        from infrastucture.repositories.brigada_repository import BrigadaRepository
        collection = get_collection(self.collection_name)
        worker = collection.find_one({"CI": ci})
        if not worker:
            return False
        # Asignar contraseña si no la tiene y se provee
        if contrasena and not worker.get("contraseña"):
            collection.update_one({"CI": ci}, {"$set": {"contraseña": contrasena}})
        # Si se pasan integrantes, crear/actualizar brigada
        if integrantes is not None:
            brigada_repo = BrigadaRepository()
            # El método update_brigada espera el id de la brigada (CI del líder), el CI del líder y los CI de los integrantes
            integrantes_ci = [i["CI"] if isinstance(i, dict) and "CI" in i else i for i in integrantes]
            # Si ya existe la brigada, actualizarla; si no, crearla
            brigada = brigada_repo.get_brigada_by_lider_ci(ci)
            if brigada:
                brigada_repo.update_brigada(ci, ci, integrantes_ci)
            else:
                brigada_repo.create_brigada(ci, integrantes_ci)
        return True

    async def create_brigada_leader(self, ci: str, nombre: str, contrasena: str = None, integrantes: list = None) -> str:
        """
        Crea un trabajador (opcionalmente con contraseña) y, si se pasan integrantes, crea la brigada con este trabajador como líder.
        """
        from infrastucture.repositories.brigada_repository import BrigadaRepository
        collection = get_collection(self.collection_name)
        # Verificar si el trabajador ya existe
        worker = collection.find_one({"CI": ci})
        if not worker:
            data = {"CI": ci, "nombre": nombre}
            if contrasena:
                data["contraseña"] = contrasena
            result = collection.insert_one(data)
        else:
            # Si ya existe, actualizar nombre y contraseña si se proveen
            update_data = {"nombre": nombre}
            if contrasena:
                update_data["contraseña"] = contrasena
            collection.update_one({"CI": ci}, {"$set": update_data})
        # Si se pasan integrantes, crear la brigada
        if integrantes is not None:
            brigada_repo = BrigadaRepository()
            integrantes_ci = [i["CI"] if isinstance(i, dict) and "CI" in i else i for i in integrantes]
            brigada = brigada_repo.get_brigada_by_lider_ci(ci)
            if brigada:
                brigada_repo.update_brigada(ci, ci, integrantes_ci)
            else:
                brigada_repo.create_brigada(ci, integrantes_ci)
        return str(ci)

    def delete_worker_by_ci(self, ci: str) -> bool:
        """
        Elimina un trabajador de la colección por su CI.
        """
        try:
            collection = get_collection(self.collection_name)
            result = collection.delete_one({"CI": ci})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"❌ Error eliminando trabajador con CI {ci}: {e}")
            raise Exception(f"Error eliminando trabajador con CI {ci}: {str(e)}")

    def update_worker_data(self, ci: str, nombre: str, nuevo_ci: str = None) -> bool:
        """
        Actualiza los datos de un trabajador (nombre y opcionalmente CI).
        """
        try:
            collection = get_collection(self.collection_name)
            update_data = {"nombre": nombre}
            if nuevo_ci:
                update_data["CI"] = nuevo_ci
            
            result = collection.update_one({"CI": ci}, {"$set": update_data})
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"❌ Error actualizando datos del trabajador con CI {ci}: {e}")
            raise Exception(f"Error actualizando datos del trabajador con CI {ci}: {str(e)}")
