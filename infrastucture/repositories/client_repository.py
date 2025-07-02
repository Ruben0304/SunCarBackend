from infrastucture.database.mongo_db.connection import get_collection
from domain.entities.cliente import Cliente


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
