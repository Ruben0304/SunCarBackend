from typing import Optional, List
import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from application.services.leads_service import LeadsService
from infrastucture.dependencies import get_leads_service
from domain.entities.lead import Lead
from presentation.schemas.requests.LeadCreateRequest import LeadCreateRequest, LeadUpdateRequest
from presentation.schemas.responses.leads_responses import (
    LeadCreateResponse, LeadGetResponse, LeadListResponse,
    LeadUpdateResponse, LeadDeleteResponse
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=LeadCreateResponse)
def crear_lead(
    lead_request: LeadCreateRequest,
    leads_service: LeadsService = Depends(get_leads_service)
):
    """
    Crear un nuevo lead.
    """
    try:
        lead_id = leads_service.create_lead(lead_request)
        # Obtener el lead creado para devolverlo en la respuesta
        lead_created = leads_service.get_lead_by_id(lead_id)
        return LeadCreateResponse(
            success=True,
            message="Lead creado exitosamente",
            data=lead_created
        )
    except Exception as e:
        logger.error(f"Error en crear_lead: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", summary="Listar leads", tags=["Leads"], response_model=LeadListResponse)
def listar_leads(
    nombre: Optional[str] = Query(None, description="Nombre del lead (búsqueda parcial)"),
    telefono: Optional[str] = Query(None, description="Teléfono del lead (búsqueda parcial)"),
    estado: Optional[str] = Query(None, description="Estado del lead"),
    fuente: Optional[str] = Query(None, description="Fuente del lead"),
    leads_service: LeadsService = Depends(get_leads_service)
):
    """Listar leads con filtros opcionales."""
    try:
        leads = leads_service.get_leads(nombre, telefono, estado, fuente)
        # Convertir los dicts a objetos Lead para la respuesta
        leads_objects = [Lead.model_validate(lead) for lead in leads]
        return LeadListResponse(
            success=True,
            message="Leads obtenidos exitosamente",
            data=leads_objects
        )
    except Exception as e:
        logger.error(f"Error en listar_leads: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{lead_id}", response_model=LeadGetResponse)
def obtener_lead_por_id(
    lead_id: str,
    leads_service: LeadsService = Depends(get_leads_service)
):
    """
    Obtener un lead por su ID.
    """
    try:
        lead = leads_service.get_lead_by_id(lead_id)
        if lead:
            return LeadGetResponse(
                success=True,
                message="Lead encontrado",
                data=lead
            )
        else:
            return LeadGetResponse(
                success=False,
                message="Lead no encontrado",
                data=None
            )
    except Exception as e:
        logger.error(f"Error en obtener_lead_por_id: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{lead_id}", response_model=LeadUpdateResponse)
def actualizar_lead(
    lead_id: str,
    update_request: LeadUpdateRequest,
    leads_service: LeadsService = Depends(get_leads_service)
):
    """
    Actualizar parcialmente un lead. Solo los campos enviados serán modificados.
    """
    try:
        # Verificar que el lead existe
        existing_lead = leads_service.get_lead_by_id(lead_id)
        if not existing_lead:
            raise HTTPException(status_code=404, detail="Lead no encontrado")

        # Actualizar el lead
        updated = leads_service.update_lead(lead_id, update_request)
        if updated:
            # Obtener el lead actualizado
            updated_lead = leads_service.get_lead_by_id(lead_id)
            return LeadUpdateResponse(
                success=True,
                message="Lead actualizado correctamente",
                data=updated_lead
            )
        else:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el lead")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en actualizar_lead: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{lead_id}", response_model=LeadDeleteResponse)
def eliminar_lead(
    lead_id: str,
    leads_service: LeadsService = Depends(get_leads_service)
):
    """
    Eliminar un lead por su ID.
    """
    try:
        deleted = leads_service.delete_lead(lead_id)
        if deleted:
            return LeadDeleteResponse(
                success=True,
                message="Lead eliminado correctamente",
                data={"lead_id": lead_id}
            )
        else:
            return LeadDeleteResponse(
                success=False,
                message="Lead no encontrado",
                data=None
            )
    except Exception as e:
        logger.error(f"Error en eliminar_lead: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/telefono/{telefono}", summary="Buscar leads por teléfono", response_model=LeadListResponse)
def buscar_leads_por_telefono(
    telefono: str,
    leads_service: LeadsService = Depends(get_leads_service)
):
    """
    Buscar leads por teléfono. Puede devolver múltiples resultados.
    """
    try:
        leads = leads_service.get_leads_by_telefono(telefono)
        return LeadListResponse(
            success=True,
            message=f"Se encontraron {len(leads)} leads con el teléfono {telefono}",
            data=leads
        )
    except Exception as e:
        logger.error(f"Error en buscar_leads_por_telefono: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{lead_id}/existe", summary="Verificar si existe un lead")
def verificar_lead_existe(
    lead_id: str,
    leads_service: LeadsService = Depends(get_leads_service)
):
    """
    Verificar si existe un lead por su ID.
    """
    try:
        exists = leads_service.verify_lead_exists(lead_id)
        return {
            "success": True,
            "message": "Lead encontrado" if exists else "Lead no encontrado",
            "exists": exists
        }
    except Exception as e:
        logger.error(f"Error en verificar_lead_existe: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))