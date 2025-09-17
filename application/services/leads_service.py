import logging
from infrastucture.repositories.leads_repository import LeadsRepository
from domain.entities.lead import Lead
from typing import Optional, List

from presentation.schemas.requests.LeadCreateRequest import LeadCreateRequest, LeadUpdateRequest


class LeadsService:
    def __init__(self, leads_repository: LeadsRepository):
        self._leads_repository = leads_repository
        self.logger = logging.getLogger(__name__)

    def create_lead(self, lead: LeadCreateRequest) -> str:
        """
        Crear un nuevo lead.
        Retorna el ID del lead creado.
        """
        self.logger.info(f"Creando lead: {lead}")
        try:
            lead_id = self._leads_repository.create_lead(lead)
            self.logger.info(f"Lead creado con ID: {lead_id}")
            return lead_id
        except Exception as e:
            self.logger.error(f"Error al crear lead: {e}")
            raise

    def get_lead_by_id(self, lead_id: str) -> Optional[Lead]:
        """
        Obtener un lead por su ID.
        """
        self.logger.info(f"Obteniendo lead por ID: {lead_id}")
        try:
            lead = self._leads_repository.find_lead_by_id(lead_id)
            self.logger.info(f"Lead encontrado: {lead}")
            return lead
        except Exception as e:
            self.logger.error(f"Error al obtener lead: {e}")
            raise

    def get_leads(self, nombre=None, telefono=None, estado=None, fuente=None):
        """
        Obtener leads con filtros opcionales.
        """
        self.logger.info(f"Listando leads con filtros: nombre={nombre}, telefono={telefono}, estado={estado}, fuente={fuente}")
        try:
            leads = self._leads_repository.get_leads(nombre, telefono, estado, fuente)
            self.logger.info(f"Leads encontrados: {len(leads)}")
            return leads
        except Exception as e:
            self.logger.error(f"Error al obtener leads: {e}")
            raise

    def update_lead(self, lead_id: str, update_data: LeadUpdateRequest) -> bool:
        """
        Actualizar un lead existente.
        Retorna True si se actualizó correctamente, False si no se encontró.
        """
        self.logger.info(f"Actualizando lead {lead_id} con datos: {update_data}")
        try:
            result = self._leads_repository.update_lead(lead_id, update_data)
            self.logger.info(f"Lead actualizado: {result}")
            return result
        except Exception as e:
            self.logger.error(f"Error al actualizar lead: {e}")
            raise

    def delete_lead(self, lead_id: str) -> bool:
        """
        Eliminar un lead por su ID.
        """
        self.logger.info(f"Eliminando lead: {lead_id}")
        try:
            result = self._leads_repository.delete_lead(lead_id)
            self.logger.info(f"Lead eliminado: {result}")
            return result
        except Exception as e:
            self.logger.error(f"Error al eliminar lead: {e}")
            raise

    def get_leads_by_telefono(self, telefono: str) -> List[Lead]:
        """
        Buscar leads por teléfono (puede haber duplicados).
        """
        self.logger.info(f"Buscando leads por teléfono: {telefono}")
        try:
            leads = self._leads_repository.find_leads_by_telefono(telefono)
            self.logger.info(f"Leads encontrados por teléfono: {len(leads)}")
            return leads
        except Exception as e:
            self.logger.error(f"Error al buscar leads por teléfono: {e}")
            raise

    def verify_lead_exists(self, lead_id: str) -> bool:
        """
        Verificar si existe un lead por su ID.
        """
        self.logger.info(f"Verificando existencia de lead: {lead_id}")
        try:
            lead = self._leads_repository.find_lead_by_id(lead_id)
            exists = lead is not None
            self.logger.info(f"Lead existe: {exists}")
            return exists
        except Exception as e:
            self.logger.error(f"Error al verificar lead: {e}")
            raise