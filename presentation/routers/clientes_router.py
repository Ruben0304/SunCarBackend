from typing import Optional, List
import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from application.services.client_service import ClientService
from infrastucture.dependencies import get_client_service
from domain.entities.cliente import Cliente
from presentation.schemas.requests.ClienteCreateRequest import ClienteCreateRequest, ClienteCreateSimpleRequest
from presentation.schemas.responses import ClienteCreateResponse, ClienteVerifyResponse, ClienteVerifyByIdentifierResponse
from presentation.schemas.requests.ClienteUpdateRequest import ClienteUpdateRequest
from presentation.schemas.requests.ClienteVerifyRequest import ClienteVerifyRequest

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=ClienteCreateResponse)
def crear_cliente(
    cliente_request: ClienteCreateRequest,
    client_service: ClientService = Depends(get_client_service)
):
    """
    Crear un nuevo cliente con información completa.
    """
    try:
        cliente = client_service.create_or_update_client(cliente_request)
        return ClienteCreateResponse(
            success=True,
            message="Cliente creado exitosamente",
            data=cliente.model_dump()  # <-- FIX: devolver dict
        )
    except Exception as e:
        logger.error(f"Error en crear_cliente: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", summary="Listar clientes", tags=["Clientes"], response_model=List[dict])
def listar_clientes(
    numero: Optional[str] = Query(None, description="Número de cliente"),
    nombre: Optional[str] = Query(None, description="Nombre del cliente (búsqueda parcial)"),
    direccion: Optional[str] = Query(None, description="Dirección del cliente (búsqueda parcial)"),
    client_service: ClientService = Depends(get_client_service)
):
    """Listar clientes con filtros opcionales."""
    try:
        clientes = client_service.get_clientes(numero, nombre, direccion)
        return clientes
    except Exception as e:
        logger.error(f"Error en listar_clientes: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{numero}/verificar", response_model=ClienteVerifyResponse)
def verificar_cliente_por_numero(
    numero: str,
    client_service: ClientService = Depends(get_client_service)
):
    """
    Verificar si existe un cliente por número.
    """
    try:
        cliente_info = client_service.verify_client_by_number(numero)
        if cliente_info:
            return ClienteVerifyResponse(
                success=True,
                message="Cliente encontrado",
                data=cliente_info
            )
        else:
            return ClienteVerifyResponse(
                success=False,
                message="Cliente no encontrado",
                data=None
            )
    except Exception as e:
        logger.error(f"Error en verificar_cliente_por_numero: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/simple", response_model=ClienteCreateResponse)
def crear_cliente_simple(
    cliente_request: ClienteCreateSimpleRequest,
    client_service: ClientService = Depends(get_client_service)
):
    """
    Crear un nuevo cliente con información mínima.
    """
    try:
        cliente = client_service.create_simple_client(cliente_request)
        return ClienteCreateResponse(
            success=True,
            message="Cliente simple creado exitosamente",
            data=cliente.model_dump()  # <-- FIX: devolver dict
        )
    except Exception as e:
        logger.error(f"Error en crear_cliente_simple: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{numero}", summary="Actualizar cliente parcialmente")
def actualizar_cliente_parcial(
    numero: str,
    update_request: ClienteUpdateRequest,
    client_service: ClientService = Depends(get_client_service)
):
    """
    Actualiza parcialmente un cliente. Solo los campos enviados serán modificados.
    """
    update_data = update_request.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar")
    try:
        updated = client_service.update_client_partial(numero, update_data)
        if updated:
            return {"success": True, "message": "Cliente actualizado correctamente"}
        else:
            return {"success": False, "message": "Cliente no encontrado o sin cambios"}
    except Exception as e:
        logger.error(f"Error en actualizar_cliente_parcial: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/verificar", response_model=ClienteVerifyByIdentifierResponse, summary="Verificar cliente por teléfono o número")
def verificar_cliente_por_identificador(
    verify_request: ClienteVerifyRequest,
    client_service: ClientService = Depends(get_client_service)
):
    """
    Verificar si existe un cliente por número de cliente o teléfono.
    
    - **identifier**: Puede ser el número de cliente o el teléfono del cliente
    
    **Respuesta exitosa**: Retorna número de cliente y nombre
    **Respuesta de error**: Mensaje detallado si el cliente no existe
    
    **Ejemplo de uso desde frontend:**
    ```javascript
    // Verificar por número de cliente
    const response = await fetch('/api/clientes/verificar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ identifier: "CLIENTE001" })
    });
    
    // Verificar por teléfono
    const response = await fetch('/api/clientes/verificar', {
        method: 'POST', 
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ identifier: "555-1234" })
    });
    ```
    """
    try:
        cliente_info = client_service.verify_client_by_identifier(verify_request.identifier)
        if cliente_info:
            return ClienteVerifyByIdentifierResponse(
                success=True,
                message="Cliente encontrado exitosamente",
                data=cliente_info
            )
        else:
            return ClienteVerifyByIdentifierResponse(
                success=False,
                message=f"No se encontró ningún cliente con el identificador: {verify_request.identifier}. Verifica que el número de cliente o teléfono sea correcto.",
                data=None
            )
    except Exception as e:
        logger.error(f"Error en verificar_cliente_por_identificador: {e}", exc_info=True)
        return ClienteVerifyByIdentifierResponse(
            success=False,
            message=f"Error interno del servidor al verificar el cliente: {str(e)}",
            data=None
        )


@router.delete("/{numero}", summary="Eliminar cliente")
def eliminar_cliente(
    numero: str,
    client_service: ClientService = Depends(get_client_service)
):
    """
    Elimina un cliente por su número.
    """
    try:
        deleted = client_service.delete_client(numero)
        if deleted:
            return {"success": True, "message": "Cliente eliminado correctamente"}
        else:
            return {"success": False, "message": "Cliente no encontrado"}
    except Exception as e:
        logger.error(f"Error en eliminar_cliente: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e)) 