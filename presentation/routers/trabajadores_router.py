from http.client import HTTPException
from typing import List

from fastapi import APIRouter, Depends, Body, Query
from pydantic import BaseModel

from application.services.worker_service import WorkerService
from infrastucture.dependencies import get_worker_service
from domain.entities.trabajador import Trabajador
from presentation.schemas.responses import (
    TrabajadorListResponse,
    TrabajadorSearchResponse,
    TrabajadorCreateResponse,
    TrabajadorBrigadaResponse
)

router = APIRouter()


class TrabajadorCreateRequest(BaseModel):
    ci: str
    nombre: str
    contrasena: str = None


class TrabajadorBrigadaRequest(BaseModel):
    ci: str
    nombre: str
    brigada_id: str
    contrasena: str = None


class ConvertirJefeRequest(BaseModel):
    contrasena: str
    integrantes: list = None


@router.get("/", response_model=TrabajadorListResponse)
async def read_workers(
        worker_service: WorkerService = Depends(get_worker_service)
):
    """
    Endpoint to get a list of all workers.
    """
    try:
        workers = await worker_service.get_all_workers()
        return TrabajadorListResponse(
            success=True,
            message="Trabajadores obtenidos exitosamente",
            data=workers
        )
    except Exception as e:
        raise HTTPException()


@router.post("/", response_model=TrabajadorCreateResponse)
async def crear_trabajador(
    request: TrabajadorCreateRequest,
    worker_service: WorkerService = Depends(get_worker_service)
):
    """
    Crear un nuevo trabajador (opcionalmente con contraseña).
    """
    try:
        worker_id = await worker_service.create_worker(request.ci, request.nombre, request.contrasena)
        return TrabajadorCreateResponse(
            success=True,
            message="Trabajador creado exitosamente",
            trabajador_id=worker_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/buscar", response_model=TrabajadorSearchResponse)
async def buscar_trabajadores(
    nombre: str = Query(..., description="Nombre a buscar"),
    worker_service: WorkerService = Depends(get_worker_service)
):
    """
    Buscar trabajadores por nombre (case-insensitive).
    """
    try:
        trabajadores = await worker_service.search_workers_by_name(nombre)
        return TrabajadorSearchResponse(
            success=True,
            message="Búsqueda completada exitosamente",
            data=trabajadores
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/jefes_brigada", response_model=TrabajadorCreateResponse)
async def crear_jefe_brigada(
    request: TrabajadorCreateRequest,
    integrantes: list = Body(default=None),
    worker_service: WorkerService = Depends(get_worker_service)
):
    """
    Crear un nuevo jefe de brigada con integrantes opcionales.
    """
    try:
        worker_id = await worker_service.create_brigada_leader(
            request.ci, 
            request.nombre, 
            request.contrasena, 
            integrantes
        )
        return TrabajadorCreateResponse(
            success=True,
            message="Jefe de brigada creado exitosamente",
            trabajador_id=worker_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{ci}/convertir_jefe", response_model=TrabajadorBrigadaResponse)
async def convertir_trabajador_a_jefe(
    ci: str,
    request: ConvertirJefeRequest,
    worker_service: WorkerService = Depends(get_worker_service)
):
    """
    Convertir un trabajador existente en jefe de brigada.
    """
    try:
        ok = await worker_service.convert_worker_to_leader(ci, request.contrasena, request.integrantes)
        if not ok:
            return TrabajadorBrigadaResponse(
                success=False,
                message="Trabajador no encontrado o ya es jefe de brigada"
            )
        return TrabajadorBrigadaResponse(
            success=True,
            message="Trabajador convertido a jefe de brigada exitosamente"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/asignar_brigada", response_model=TrabajadorBrigadaResponse)
async def crear_trabajador_y_asignar_brigada(
    request: TrabajadorBrigadaRequest,
    worker_service: WorkerService = Depends(get_worker_service)
):
    """
    Crear un trabajador y asignarlo a una brigada existente.
    """
    try:
        ok = await worker_service.create_worker_and_assign_brigada(
            request.ci, 
            request.nombre, 
            request.brigada_id, 
            request.contrasena
        )
        if not ok:
            return TrabajadorBrigadaResponse(
                success=False,
                message="Brigada no encontrada o trabajador ya existe"
            )
        return TrabajadorBrigadaResponse(
            success=True,
            message="Trabajador creado y asignado a brigada exitosamente"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 