import logging
from infrastucture.database.mongo_db.connection import get_collection
from domain.entities.cliente import Cliente
from typing import Optional

from presentation.schemas.requests.ClienteCreateRequest import ClienteCreateRequest


class ClientRepository:
    def __init__(self):
        self.collection_name = "clientes"
        self.logger = logging.getLogger(__name__)

    def create_or_update_client(self, cliente: ClienteCreateRequest) -> ClienteCreateRequest:
        """
        Crear un nuevo cliente o actualizar si ya existe basado en el número de cliente.
        Usa upsert de MongoDB para hacer insert or update en una sola operación.
        """
        collection = get_collection(self.collection_name)
        cliente_dict = cliente.model_dump()
        self.logger.info(f"Upsert cliente: {cliente_dict}")
        try:
            result = collection.update_one(
                {"numero": cliente.numero},
                {"$set": cliente_dict},
                upsert=True
            )
            self.logger.info(f"Resultado upsert: matched={result.matched_count}, modified={result.modified_count}, upserted_id={result.upserted_id}")
            return cliente
        except Exception as e:
            self.logger.error(f"Error en upsert cliente: {e}")
            raise

    def find_client_by_number(self, numero: str) -> Optional[Cliente]:
        """
        Buscar un cliente por su número.
        Retorna el cliente si existe, None si no existe.
        """
        collection = get_collection(self.collection_name)
        self.logger.info(f"Buscando cliente por número: {numero}")
        try:
            cliente_doc = collection.find_one({"numero": numero})
            if cliente_doc:
                self.logger.info(f"Cliente encontrado: {cliente_doc}")
                return Cliente.model_validate(cliente_doc)
            self.logger.info("Cliente no encontrado")
            return None
        except Exception as e:
            self.logger.error(f"Error al buscar cliente: {e}")
            raise

    def update_client_partial(self, numero: str, update_data: dict) -> bool:
        collection = get_collection(self.collection_name)
        self.logger.info(f"Actualizando cliente {numero} con datos: {update_data}")
        try:
            result = collection.update_one(
                {"numero": numero},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            self.logger.error(f"Error al actualizar cliente: {e}")
            raise

    def get_clientes(self, numero=None, nombre=None, direccion=None):
        collection = get_collection(self.collection_name)
        query = {}
        if numero:
            query["numero"] = numero
        if nombre:
            query["nombre"] = {"$regex": nombre, "$options": "i"}
        if direccion:
            query["direccion"] = {"$regex": direccion, "$options": "i"}
        self.logger.info(f"Buscando clientes con query: {query}")
        try:
            cursor = collection.find(query)
            clientes = []
            for doc in cursor:
                doc["id"] = str(doc.pop("_id"))
                clientes.append(doc)
            # Ordenar por los últimos 4 dígitos del campo 'numero'
            clientes.sort(key=lambda c: int(c["numero"][-4:]))
            self.logger.info(f"Clientes encontrados: {len(clientes)}")
            return clientes
        except Exception as e:
            self.logger.error(f"Error al obtener clientes: {e}")
            raise

    def delete_client(self, numero: str) -> bool:
        """
        Eliminar un cliente por su número.
        Retorna True si se eliminó correctamente, False si no se encontró.
        """
        collection = get_collection(self.collection_name)
        self.logger.info(f"Eliminando cliente con número: {numero}")
        try:
            result = collection.delete_one({"numero": numero})
            deleted = result.deleted_count > 0
            self.logger.info(f"Cliente eliminado: {deleted}")
            return deleted
        except Exception as e:
            self.logger.error(f"Error al eliminar cliente: {e}")
            raise
