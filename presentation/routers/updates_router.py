from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from domain.entities.form import Form
from domain.entities.update import DataUpdateRequest, DataUpdateResponse, AppUpdateRequest, AppUpdateResponse
from application.services.form_service import FormService
from application.services.update_service import UpdateService
from infrastucture.dependencies import get_form_service, get_update_service
from presentation.schemas.responses import UpdateStatusResponse

router = APIRouter()


@router.post("/data", response_model=DataUpdateResponse)
async def check_data_updates(
    request: DataUpdateRequest,
    update_service: UpdateService = Depends(get_update_service)
) -> DataUpdateResponse:
    """
    Verifica si los datos de la aplicación están actualizados.
    
    Args:
        request: Contiene la última fecha de actualización conocida por la app
        update_service: Servicio para manejar actualizaciones
    
    Returns:
        DataUpdateResponse: Indica si está actualizado y qué entidades necesitan actualización
    """
    try:
        return update_service.check_data_updates(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al verificar actualizaciones: {str(e)}")


@router.post("/application", response_model=AppUpdateResponse)
async def check_app_updates(
    request: AppUpdateRequest,
    update_service: UpdateService = Depends(get_update_service)
) -> AppUpdateResponse:
    """
    Verifica si la aplicación está actualizada.
    
    Args:
        request: Contiene la versión actual y plataforma de la app
        update_service: Servicio para manejar actualizaciones
    
    Returns:
        AppUpdateResponse: Indica si está actualizada y proporciona información de descarga si es necesario
    """
    try:
        return update_service.check_app_updates(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al verificar actualización de app: {str(e)}")


@router.get("/status", response_model=UpdateStatusResponse)
async def get_update_status(
    update_service: UpdateService = Depends(get_update_service)
):
    """
    Obtiene el estado general de las actualizaciones del sistema.
    Útil para monitoreo y debugging.
    """
    try:
        return UpdateStatusResponse(
            system_status="operational",
            last_check=datetime.now().isoformat(),
            available_entities=["materiales", "trabajadores", "clientes"],
            app_versions={
                "android": update_service.app_versions["android"]["latest_version"],
                "ios": update_service.app_versions["ios"]["latest_version"]
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estado: {str(e)}")

