from infrastucture.database.mongo_db.connection import get_collection
from domain.entities.cliente import Cliente
from typing import Optional


class ClientRepository:
    def __init__(self):
        self.collection_name = "clientes"

    async def create_or_update_client(self, cliente: Cliente) -> Cliente:
        """
        Crear un nuevo cliente o actualizar si ya existe basado en el número de cliente.
        Usa upsert de MongoDB para hacer insert or update en una sola operación.
        """
        collection = get_collection(self.collection_name)
        
        # Convertir el cliente a diccionario
        cliente_dict = cliente.model_dump()
        
        # Realizar upsert basado en el número de cliente
        result = collection.update_one(
            {"numero": cliente.numero},  # Filtro para buscar por número
            {"$set": cliente_dict},      # Datos a insertar/actualizar
            upsert=True                  # Crear si no existe, actualizar si existe
        )
        
        return cliente

    async def find_client_by_number(self, numero: str) -> Optional[Cliente]:
        """
        Buscar un cliente por su número.
        Retorna el cliente si existe, None si no existe.
        """
        collection = get_collection(self.collection_name)
        
        # Buscar el cliente por número
        cliente_doc = collection.find_one({"numero": numero})
        
        if cliente_doc:
            # Convertir el documento de MongoDB a la entidad Cliente
            return Cliente.model_validate(cliente_doc)
        
        return None
