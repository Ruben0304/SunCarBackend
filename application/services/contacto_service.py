import logging
from infrastucture.repositories.contacto_repository import ContactoRepository
from domain.entities.contacto import Contacto
from typing import Optional, List


class ContactoService:
    def __init__(self, contacto_repository: ContactoRepository):
        self._contacto_repository = contacto_repository
        self.logger = logging.getLogger(__name__)

    def create_contacto(self, contacto: Contacto) -> Contacto:
        """
        Crear un nuevo contacto.
        """
        self.logger.info(f"Creando contacto: {contacto}")
        try:
            result = self._contacto_repository.create_contacto(contacto)
            self.logger.info(f"Contacto creado: {result}")
            return result
        except Exception as e:
            self.logger.error(f"Error al crear contacto: {e}")
            raise

    def find_contacto_by_id(self, contacto_id: str) -> Optional[Contacto]:
        """
        Buscar un contacto por su ID.
        """
        self.logger.info(f"Buscando contacto por ID: {contacto_id}")
        try:
            contacto = self._contacto_repository.find_contacto_by_id(contacto_id)
            self.logger.info(f"Contacto encontrado: {contacto}")
            return contacto
        except Exception as e:
            self.logger.error(f"Error al buscar contacto: {e}")
            raise

    def update_contacto(self, contacto_id: str, contacto: Contacto) -> bool:
        """
        Actualizar un contacto existente.
        """
        self.logger.info(f"Actualizando contacto {contacto_id}: {contacto}")
        try:
            result = self._contacto_repository.update_contacto(contacto_id, contacto)
            self.logger.info(f"Contacto actualizado: {result}")
            return result
        except Exception as e:
            self.logger.error(f"Error al actualizar contacto: {e}")
            raise

    def get_all_contactos(self) -> List[Contacto]:
        """
        Obtener todos los contactos.
        """
        self.logger.info("Obteniendo todos los contactos")
        try:
            contactos = self._contacto_repository.get_all_contactos()
            self.logger.info(f"Contactos obtenidos: {len(contactos)}")
            return contactos
        except Exception as e:
            self.logger.error(f"Error al obtener contactos: {e}")
            raise

    def delete_contacto(self, contacto_id: str) -> bool:
        """
        Eliminar un contacto por su ID.
        """
        self.logger.info(f"Eliminando contacto: {contacto_id}")
        try:
            result = self._contacto_repository.delete_contacto(contacto_id)
            self.logger.info(f"Contacto eliminado: {result}")
            return result
        except Exception as e:
            self.logger.error(f"Error al eliminar contacto: {e}")
            raise
