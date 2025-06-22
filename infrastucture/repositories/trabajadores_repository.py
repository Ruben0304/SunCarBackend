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
