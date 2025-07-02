from infrastucture.repositories.client_repository import ClientRepository
from domain.entities.cliente import Cliente


class ClientService:
    def __init__(self, client_repository: ClientRepository):
        self._client_repository = client_repository

    async def create_or_update_client(self, cliente: Cliente) -> Cliente:
        """
        Crear un nuevo cliente o actualizar si ya existe.
        """
        return await self._client_repository.create_or_update_client(cliente)
