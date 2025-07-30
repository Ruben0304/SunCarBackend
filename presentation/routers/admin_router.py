from typing import List

from fastapi import APIRouter, Depends, HTTPException
from domain.entities.form import Form
from domain.entities.update import AppVersionConfig
from application.services.form_service import FormService
from infrastucture.dependencies import get_form_service, get_update_repository
from infrastucture.repositories.update_repository import UpdateRepository

router = APIRouter()


# ====================== APP VERSION MANAGEMENT ENDPOINTS ======================

@router.get("/app-versions", response_model=List[AppVersionConfig])
async def get_all_app_versions(
    update_repo: UpdateRepository = Depends(get_update_repository)
):
    """
    Obtiene todas las configuraciones de versiones de app
    """
    try:
        return update_repo.get_all_app_version_configs()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/app-versions/{platform}", response_model=AppVersionConfig)
async def get_app_version(
    platform: str,
    update_repo: UpdateRepository = Depends(get_update_repository)
):
    """
    Obtiene la configuración de versión para una plataforma específica
    """
    try:
        config = update_repo.get_app_version_config(platform)
        if not config:
            raise HTTPException(status_code=404, detail=f"No se encontró configuración para la plataforma: {platform}")
        return config
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/app-versions", response_model=dict)
async def create_app_version(
    config: AppVersionConfig,
    update_repo: UpdateRepository = Depends(get_update_repository)
):
    """
    Crea o actualiza una configuración de versión de app (upsert)
    """
    try:
        config_id = update_repo.upsert_app_version_config(config)
        return {"id": config_id, "message": f"Configuración para {config.platform} creada/actualizada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/app-versions/{platform}", response_model=dict)
async def update_app_version(
    platform: str,
    config: AppVersionConfig,
    update_repo: UpdateRepository = Depends(get_update_repository)
):
    """
    Actualiza la configuración de versión para una plataforma específica
    """
    try:
        success = update_repo.update_app_version_config(platform, config)
        if not success:
            raise HTTPException(status_code=404, detail=f"No se encontró configuración para la plataforma: {platform}")
        return {"message": f"Configuración para {platform} actualizada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/app-versions/{platform}", response_model=dict)
async def delete_app_version(
    platform: str,
    update_repo: UpdateRepository = Depends(get_update_repository)
):
    """
    Elimina la configuración de versión para una plataforma específica
    """
    try:
        success = update_repo.delete_app_version_config(platform)
        if not success:
            raise HTTPException(status_code=404, detail=f"No se encontró configuración para la plataforma: {platform}")
        return {"message": f"Configuración para {platform} eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
