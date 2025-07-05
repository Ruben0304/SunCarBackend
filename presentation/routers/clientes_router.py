from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from application.services.client_service import ClientService
from infrastucture.dependencies import get_client_service
from domain.entities.cliente import Cliente
from presentation.schemas.requests.ClienteCreateRequest import ClienteCreateRequest, ClienteCreateSimpleRequest
from presentation.schemas.responses import ClienteCreateResponse, ClienteVerifyResponse

router = APIRouter()


@router.post("/", response_model=ClienteCreateResponse)
async def crear_cliente(
    cliente_request: ClienteCreateRequest,
    client_service: ClientService = Depends(get_client_service)
):
    """
    Crear un nuevo cliente con información completa.
    """
    try:
        cliente = await client_service.create_client(cliente_request)
        return ClienteCreateResponse(
            success=True,
            message="Cliente creado exitosamente",
            data=cliente
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", summary="Listar clientes", tags=["Clientes"], response_model=List[dict])
def listar_clientes(
    numero: Optional[str] = Query(None, description="Número de cliente"),
    nombre: Optional[str] = Query(None, description="Nombre del cliente (búsqueda parcial)"),
    direccion: Optional[str] = Query(None, description="Dirección del cliente (búsqueda parcial)"),
    client_service: ClientService = Depends(get_client_service)
):
    """Listar clientes con filtros opcionales."""
    clientes = client_service.get_clientes(numero, nombre, direccion)
    return clientes


@router.get("/{numero}/verificar", response_model=ClienteVerifyResponse)
async def verificar_cliente_por_numero(
    numero: str,
    client_service: ClientService = Depends(get_client_service)
):
    """
    Verificar si existe un cliente por número.
    """
    try:
        cliente_info = await client_service.verify_client_by_number(numero)
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
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/simple", response_model=ClienteCreateResponse)
async def crear_cliente_simple(
    cliente_request: ClienteCreateSimpleRequest,
    client_service: ClientService = Depends(get_client_service)
):
    """
    Crear un nuevo cliente con información mínima.
    """
    try:
        cliente = await client_service.create_simple_client(cliente_request)
        return ClienteCreateResponse(
            success=True,
            message="Cliente simple creado exitosamente",
            data=cliente
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 