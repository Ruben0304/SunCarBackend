from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel

from application.services.worker_service import WorkerService
from infrastucture.dependencies import get_worker_service

router = APIRouter()

class ChangePasswordRequest(BaseModel):
    ci: str
    nueva_contrasena: str

@router.post("/cambiar_contrasena", response_model=bool)
async def cambiar_contrasena(
    data: ChangePasswordRequest,
    worker_service: WorkerService = Depends(get_worker_service)
):
    """
    Cambia la contraseña de un trabajador dado el CI y la nueva contraseña.
    """
    try:
        ok = await worker_service.set_worker_password(data.ci, data.nueva_contrasena)
        if not ok:
            raise HTTPException(status_code=404, detail="Trabajador no encontrado o sin cambios")
        return ok
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 