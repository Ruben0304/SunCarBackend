import logging
from infrastucture.repositories.client_repository import ClientRepository
from domain.entities.cliente import Cliente
from typing import Optional

from presentation.schemas.requests.ClienteCreateRequest import ClienteCreateRequest


class ClientService:
    def __init__(self, client_repository: ClientRepository):
        self._client_repository = client_repository
        self.logger = logging.getLogger(__name__)

    def create_or_update_client(self, cliente: ClienteCreateRequest) -> ClienteCreateRequest:
        """
        Crear un nuevo cliente o actualizar si ya existe.
        """
        self.logger.info(f"Creando o actualizando cliente: {cliente}")
        try:
            result = self._client_repository.create_or_update_client(cliente)
            self.logger.info(f"Cliente creado/actualizado: {result}")
            return result
        except Exception as e:
            self.logger.error(f"Error al crear o actualizar cliente: {e}")
            raise

    def find_client_by_number(self, numero: str) -> Optional[Cliente]:
        """
        Buscar un cliente por su número.
        Retorna el cliente si existe, None si no existe.
        """
        self.logger.info(f"Buscando cliente por número: {numero}")
        try:
            cliente = self._client_repository.find_client_by_number(numero)
            self.logger.info(f"Cliente encontrado: {cliente}")
            return cliente
        except Exception as e:
            self.logger.error(f"Error al buscar cliente: {e}")
            raise

    def verify_client_by_number(self, numero: str) -> Optional[dict]:
        """
        Verifica si existe un cliente por número y retorna el dict serializable.
        """
        self.logger.info(f"Verificando cliente por número: {numero}")
        cliente = self._client_repository.find_client_by_number(numero)
        if cliente:
            return cliente.model_dump()
        return None

    def create_simple_client(self, cliente_simple_request) -> ClienteCreateRequest:
        """
        Crear un cliente con información mínima.
        """
        self.logger.info(f"Creando cliente simple: {cliente_simple_request}")
        # Rellenar latitud/longitud si no están
        data = cliente_simple_request.model_dump()
        if data.get('latitud') is None:
            data['latitud'] = ''
        if data.get('longitud') is None:
            data['longitud'] = ''
        cliente_full = ClienteCreateRequest(**data)
        return self.create_or_update_client(cliente_full)

    def get_clientes(self, numero=None, nombre=None, direccion=None):
        self.logger.info(f"Listando clientes con filtros: numero={numero}, nombre={nombre}, direccion={direccion}")
        return self._client_repository.get_clientes(numero, nombre, direccion)

    def update_client_partial(self, numero: str, update_data: dict) -> bool:
        return self._client_repository.update_client_partial(numero, update_data)

    def delete_client(self, numero: str) -> bool:
        """
        Eliminar un cliente por su número.
        """
        self.logger.info(f"Eliminando cliente: {numero}")
        try:
            result = self._client_repository.delete_client(numero)
            self.logger.info(f"Cliente eliminado: {result}")
            return result
        except Exception as e:
            self.logger.error(f"Error al eliminar cliente: {e}")
            raise
