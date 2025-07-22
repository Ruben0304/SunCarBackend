from http.client import HTTPException
from typing import List

from fastapi import APIRouter, Depends, Body, Query, HTTPException, Path
from pydantic import BaseModel

from application.services.worker_service import WorkerService
from infrastucture.dependencies import get_worker_service, get_brigada_service
from application.services.brigada_service import BrigadaService
from domain.entities.trabajador import Trabajador
from presentation.schemas.responses import (
    TrabajadorListResponse,
    TrabajadorSearchResponse,
    TrabajadorCreateResponse,
    TrabajadorBrigadaResponse,
    HoursWorkedResponse
)
from presentation.schemas.responses.reportes_responses import AllWorkersHoursWorkedResponse

router = APIRouter()


class TrabajadorCreateRequest(BaseModel):
    ci: str
    nombre: str
    contrasena: str = None
    integrantes: list = None


class TrabajadorBrigadaRequest(BaseModel):
    ci: str
    nombre: str
    brigada_id: str
    contrasena: str = None


class ConvertirJefeRequest(BaseModel):
    contrasena: str
    integrantes: list = None


class TrabajadorUpdateRequest(BaseModel):
    nombre: str
    nuevo_ci: str = None


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
            request.integrantes
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


@router.get(
    "/horas-trabajadas/{ci}",
    response_model=HoursWorkedResponse,
    status_code=200,
    summary="Obtener Horas Trabajadas por CI",
    description="""
    Endpoint para obtener el total de horas trabajadas por una persona en un rango de fechas específico.
    
    Este endpoint calcula las horas trabajadas basándose en:
    - **CI**: Cédula de identidad de la persona
    - **Fecha Inicio**: Fecha de inicio del rango (formato: YYYY-MM-DD)
    - **Fecha Fin**: Fecha de fin del rango (formato: YYYY-MM-DD)
    
    El cálculo incluye todas las actividades donde la persona aparece como líder o integrante de brigada.
    """,
    response_description="Horas trabajadas obtenidas exitosamente",
    tags=["Trabajadores - Horas Trabajadas"]
)
async def get_hours_worked_by_ci(
    ci: str,
    fecha_inicio: str,
    fecha_fin: str,
    worker_service: WorkerService = Depends(get_worker_service)
):
    try:
        total_horas = worker_service.get_hours_worked_by_ci(ci, fecha_inicio, fecha_fin)
        
        return HoursWorkedResponse(
            success=True,
            message=f"Horas trabajadas obtenidas correctamente para CI {ci}",
            data={
                "ci": ci,
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin,
                "total_horas": total_horas
            }
        )
    except Exception as e:
        return HoursWorkedResponse(
            success=False,
            message=f"Error obteniendo horas trabajadas: {str(e)}",
            data={}
        )


@router.get(
    "/horas-trabajadas-todos",
    response_model=AllWorkersHoursWorkedResponse,
    status_code=200,
    summary="Obtener Horas Trabajadas de Todos los Trabajadores",
    description="""
    Endpoint para obtener el total de horas trabajadas de todos los trabajadores en un rango de fechas específico.
    
    Este endpoint calcula las horas trabajadas de todos los trabajadores basándose en:
    - **Fecha Inicio**: Fecha de inicio del rango (formato: YYYY-MM-DD)
    - **Fecha Fin**: Fecha de fin del rango (formato: YYYY-MM-DD)
    
    El cálculo incluye todas las actividades donde cada persona aparece como líder o integrante de brigada.
    Los resultados se ordenan por total de horas trabajadas de mayor a menor.
    """,
    response_description="Horas trabajadas de todos los trabajadores obtenidas exitosamente",
    tags=["Trabajadores - Horas Trabajadas"]
)
async def get_all_workers_hours_worked(
    fecha_inicio: str,
    fecha_fin: str,
    worker_service: WorkerService = Depends(get_worker_service)
):
    try:
        trabajadores = worker_service.get_all_workers_hours_worked(fecha_inicio, fecha_fin)
        
        return AllWorkersHoursWorkedResponse(
            success=True,
            message=f"Horas trabajadas de todos los trabajadores obtenidas correctamente",
            data={
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin,
                "total_trabajadores": len(trabajadores),
                "trabajadores": trabajadores
            }
        )
    except Exception as e:
        return AllWorkersHoursWorkedResponse(
            success=False,
            message=f"Error obteniendo horas trabajadas de todos los trabajadores: {str(e)}",
            data={}
        ) 


@router.put("/{ci}")
async def actualizar_trabajador(
    ci: str = Path(..., description="Cédula de identidad del trabajador a actualizar"),
    request: TrabajadorUpdateRequest = Body(...),
    worker_service: WorkerService = Depends(get_worker_service)
):
    """
    Actualiza los datos de un trabajador (nombre y opcionalmente CI).
    """
    try:
        actualizado = await worker_service.update_worker_data(ci, request.nombre, request.nuevo_ci)
        if actualizado:
            return {"success": True, "message": f"Trabajador con CI {ci} actualizado exitosamente."}
        else:
            raise HTTPException(status_code=404, detail=f"Trabajador con CI {ci} no encontrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{ci}/brigada/{brigada_id}")
async def eliminar_trabajador_de_brigada(
    ci: str = Path(..., description="Cédula de identidad del trabajador"),
    brigada_id: str = Path(..., description="ID de la brigada"),
    worker_service: WorkerService = Depends(get_worker_service)
):
    """
    Elimina un trabajador de una brigada específica.
    """
    try:
        eliminado = await worker_service.remove_worker_from_brigada(brigada_id, ci)
        if eliminado:
            return {"success": True, "message": f"Trabajador con CI {ci} eliminado de la brigada exitosamente."}
        else:
            raise HTTPException(status_code=404, detail="Trabajador o brigada no encontrados.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{ci}")
async def eliminar_trabajador(
    ci: str = Path(..., description="Cédula de identidad del trabajador a eliminar"),
    worker_service: WorkerService = Depends(get_worker_service)
):
    """
    Elimina un trabajador dado su CI.
    """
    try:
        eliminado = await worker_service.delete_worker_by_ci(ci)
        if eliminado:
            return {"success": True, "message": f"Trabajador con CI {ci} eliminado exitosamente."}
        else:
            raise HTTPException(status_code=404, detail=f"Trabajador con CI {ci} no encontrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 


@router.delete("/{ci}/contrasena")
async def eliminar_contrasena_trabajador(
    ci: str = Path(..., description="Cédula de identidad del trabajador al que se le eliminará la contraseña"),
    worker_service: WorkerService = Depends(get_worker_service)
):
    """
    Elimina la contraseña de un trabajador (lo convierte en trabajador normal).
    """
    try:
        eliminado = await worker_service.remove_worker_password(ci)
        if eliminado:
            return {"success": True, "message": f"Contraseña eliminada para el trabajador con CI {ci}."}
        else:
            raise HTTPException(status_code=404, detail=f"Trabajador con CI {ci} no encontrado o ya no tiene contraseña.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 