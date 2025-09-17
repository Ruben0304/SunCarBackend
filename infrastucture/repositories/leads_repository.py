import logging
from bson import ObjectId
from infrastucture.database.mongo_db.connection import get_collection
from domain.entities.lead import Lead
from typing import Optional, List

from presentation.schemas.requests.LeadCreateRequest import LeadCreateRequest, LeadUpdateRequest


class LeadsRepository:
    def __init__(self):
        self.collection_name = "leads"
        self.logger = logging.getLogger(__name__)

    def create_lead(self, lead: LeadCreateRequest) -> str:
        """
        Crear un nuevo lead.
        Retorna el ID del lead creado.
        """
        collection = get_collection(self.collection_name)
        lead_dict = lead.model_dump()
        self.logger.info(f"Creando lead: {lead_dict}")
        try:
            result = collection.insert_one(lead_dict)
            self.logger.info(f"Lead creado con ID: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            self.logger.error(f"Error al crear lead: {e}")
            raise

    def find_lead_by_id(self, lead_id: str) -> Optional[Lead]:
        """
        Buscar un lead por su ID.
        Retorna el lead si existe, None si no existe.
        """
        collection = get_collection(self.collection_name)
        self.logger.info(f"Buscando lead por ID: {lead_id}")
        try:
            lead_doc = collection.find_one({"_id": ObjectId(lead_id)})
            if lead_doc:
                lead_doc["id"] = str(lead_doc.pop("_id"))
                self.logger.info(f"Lead encontrado: {lead_doc}")
                return Lead.model_validate(lead_doc)
            self.logger.info("Lead no encontrado")
            return None
        except Exception as e:
            self.logger.error(f"Error al buscar lead: {e}")
            raise

    def get_leads(self, nombre=None, telefono=None, estado=None, fuente=None):
        """
        Obtener leads con filtros opcionales.
        """
        collection = get_collection(self.collection_name)
        query = {}
        if nombre:
            query["nombre"] = {"$regex": nombre, "$options": "i"}
        if telefono:
            query["telefono"] = {"$regex": telefono, "$options": "i"}
        if estado:
            query["estado"] = estado
        if fuente:
            query["fuente"] = fuente

        self.logger.info(f"Buscando leads con query: {query}")
        try:
            cursor = collection.find(query)
            leads = []
            for doc in cursor:
                doc["id"] = str(doc.pop("_id"))
                leads.append(doc)
            # Ordenar por fecha de contacto más reciente
            leads.sort(key=lambda l: l.get("fecha_contacto", ""), reverse=True)
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
        collection = get_collection(self.collection_name)
        # Filtrar campos que no son None
        update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}
        self.logger.info(f"Actualizando lead {lead_id} con datos: {update_dict}")
        try:
            result = collection.update_one(
                {"_id": ObjectId(lead_id)},
                {"$set": update_dict}
            )
            updated = result.modified_count > 0
            self.logger.info(f"Lead actualizado: {updated}")
            return updated
        except Exception as e:
            self.logger.error(f"Error al actualizar lead: {e}")
            raise

    def delete_lead(self, lead_id: str) -> bool:
        """
        Eliminar un lead por su ID.
        Retorna True si se eliminó correctamente, False si no se encontró.
        """
        collection = get_collection(self.collection_name)
        self.logger.info(f"Eliminando lead con ID: {lead_id}")
        try:
            result = collection.delete_one({"_id": ObjectId(lead_id)})
            deleted = result.deleted_count > 0
            self.logger.info(f"Lead eliminado: {deleted}")
            return deleted
        except Exception as e:
            self.logger.error(f"Error al eliminar lead: {e}")
            raise

    def find_leads_by_telefono(self, telefono: str) -> List[Lead]:
        """
        Buscar leads por teléfono (puede haber duplicados).
        """
        collection = get_collection(self.collection_name)
        self.logger.info(f"Buscando leads por teléfono: {telefono}")
        try:
            cursor = collection.find({"telefono": telefono})
            leads = []
            for doc in cursor:
                doc["id"] = str(doc.pop("_id"))
                leads.append(Lead.model_validate(doc))
            self.logger.info(f"Leads encontrados por teléfono: {len(leads)}")
            return leads
        except Exception as e:
            self.logger.error(f"Error al buscar leads por teléfono: {e}")
            raise