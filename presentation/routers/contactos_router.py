from typing import List
import logging

from fastapi import APIRouter, Depends, HTTPException

from application.services.contacto_service import ContactoService
from infrastucture.dependencies import get_contacto_service
from domain.entities.contacto import Contacto
from presentation.schemas.requests.ContactoRequest import ContactoCreateRequest, ContactoUpdateRequest
from presentation.schemas.responses.contactos_responses import (
    ContactoCreateResponse,
    ContactoUpdateResponse,
    ContactoGetResponse,
    ContactoListResponse,
    ContactoDeleteResponse
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=ContactoCreateResponse, tags=["Contactos"])
def crear_contacto(
    contacto_request: ContactoCreateRequest,
    contacto_service: ContactoService = Depends(get_contacto_service)
):
    """
    Crear un nuevo contacto con teléfono, correo y dirección.
    """
    try:
        contacto = Contacto(**contacto_request.model_dump())
        contacto_creado = contacto_service.create_contacto(contacto)
        return ContactoCreateResponse(
            success=True,
            message="Contacto creado exitosamente",
            data=contacto_creado
        )
    except Exception as e:
        logger.error(f"Error en crear_contacto: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=ContactoListResponse, tags=["Contactos"])
def listar_contactos(
    contacto_service: ContactoService = Depends(get_contacto_service)
):
    """
    Obtener todos los contactos.
    """
    try:
        contactos = contacto_service.get_all_contactos()
        return ContactoListResponse(
            success=True,
            message=f"Se encontraron {len(contactos)} contactos",
            data=contactos
        )
    except Exception as e:
        logger.error(f"Error en listar_contactos: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/first", response_model=ContactoGetResponse, tags=["Contactos"])
def obtener_primer_contacto(
    contacto_service: ContactoService = Depends(get_contacto_service)
):
    """
    Obtener el primer contacto de la base de datos.
    """
    try:
        contacto = contacto_service.get_first_contacto()
        if not contacto:
            raise HTTPException(status_code=404, detail="No se encontraron contactos")
        
        return ContactoGetResponse(
            success=True,
            message="Primer contacto encontrado",
            data=contacto
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en obtener_primer_contacto: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{contacto_id}", response_model=ContactoGetResponse, tags=["Contactos"])
def obtener_contacto(
    contacto_id: str,
    contacto_service: ContactoService = Depends(get_contacto_service)
):
    """
    Obtener un contacto específico por su ID.
    """
    try:
        contacto = contacto_service.find_contacto_by_id(contacto_id)
        if not contacto:
            raise HTTPException(status_code=404, detail="Contacto no encontrado")
        
        return ContactoGetResponse(
            success=True,
            message="Contacto encontrado",
            data=contacto
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en obtener_contacto: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{contacto_id}", response_model=ContactoUpdateResponse, tags=["Contactos"])
def actualizar_contacto(
    contacto_id: str,
    contacto_request: ContactoUpdateRequest,
    contacto_service: ContactoService = Depends(get_contacto_service)
):
    """
    Actualizar un contacto existente.
    """
    try:
        # Verificar que el contacto existe
        contacto_existente = contacto_service.find_contacto_by_id(contacto_id)
        if not contacto_existente:
            raise HTTPException(status_code=404, detail="Contacto no encontrado")
        
        # Crear el objeto contacto con el ID existente
        contacto_actualizado = Contacto(
            id=contacto_id,
            **contacto_request.model_dump()
        )
        
        success = contacto_service.update_contacto(contacto_id, contacto_actualizado)
        if not success:
            raise HTTPException(status_code=500, detail="Error al actualizar el contacto")
        
        # Obtener el contacto actualizado
        contacto_final = contacto_service.find_contacto_by_id(contacto_id)
        
        return ContactoUpdateResponse(
            success=True,
            message="Contacto actualizado exitosamente",
            data=contacto_final
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en actualizar_contacto: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{contacto_id}", response_model=ContactoDeleteResponse, tags=["Contactos"])
def eliminar_contacto(
    contacto_id: str,
    contacto_service: ContactoService = Depends(get_contacto_service)
):
    """
    Eliminar un contacto por su ID.
    """
    try:
        # Verificar que el contacto existe
        contacto_existente = contacto_service.find_contacto_by_id(contacto_id)
        if not contacto_existente:
            raise HTTPException(status_code=404, detail="Contacto no encontrado")
        
        success = contacto_service.delete_contacto(contacto_id)
        if not success:
            raise HTTPException(status_code=500, detail="Error al eliminar el contacto")
        
        return ContactoDeleteResponse(
            success=True,
            message="Contacto eliminado exitosamente"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en eliminar_contacto: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
