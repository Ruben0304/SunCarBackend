from infrastucture.repositories.client_repository import ClientRepository
from domain.entities.cliente import Cliente
from typing import Optional

from presentation.schemas.requests.ClienteCreateRequest import ClienteCreateRequest


class ClientService:
    def __init__(self, client_repository: ClientRepository):
        self._client_repository = client_repository

    async def create_or_update_client(self, cliente: ClienteCreateRequest) -> ClienteCreateRequest:
        """
        Crear un nuevo cliente o actualizar si ya existe.
        """
        return await self._client_repository.create_or_update_client(cliente)

    async def find_client_by_number(self, numero: str) -> Optional[Cliente]:
        """
        Buscar un cliente por su número.
        Retorna el cliente si existe, None si no existe.
        """
        return await self._client_repository.find_client_by_number(numero)

    def get_clientes(self, numero=None, nombre=None, direccion=None):
        return self._client_repository.get_clientes(numero, nombre, direccion)
