from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from application.services.worker_service import WorkerService
from infrastucture.dependencies import get_worker_service, get_brigada_repository
from infrastucture.repositories.brigada_repository import BrigadaRepository
from presentation.schemas.requests.InversionFormRequest import BrigadaRequest, TeamMember
from domain.entities.brigada import Brigada
from domain.entities.trabajador import Trabajador

router = APIRouter()


# Aquí irán los endpoints de brigadas y trabajadores

@router.get("/brigadas", response_model=List[Brigada])
async def listar_brigadas(
        brigada_repo: BrigadaRepository = Depends(get_brigada_repository),
        search: str = None
):
    """
    Listar todas las brigadas (con jefe y trabajadores). Permite búsqueda opcional por nombre de jefe o integrantes.
    """
    try:
        if search:
            # Buscar por nombre de líder o integrantes
            brigadas = brigada_repo.get_all_brigadas()
            filtradas = []
            for b in brigadas:
                if search.lower() in b.lider.nombre.lower() or any(
                        search.lower() in i.nombre.lower() for i in b.integrantes):
                    filtradas.append(b)
            return filtradas
        return brigada_repo.get_all_brigadas()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/brigadas/{brigada_id}", response_model=Brigada)
async def obtener_brigada(
        brigada_id: str,
        brigada_repo: BrigadaRepository = Depends(get_brigada_repository)
):
    """
    Obtener los detalles de una brigada específica.
    """
    try:
        # Buscar por id en la view (requiere adaptación si la view no tiene _id)
        # Aquí se asume que el id es el CI del líder
        brigada = brigada_repo.get_brigada_by_lider_ci(brigada_id)
        if not brigada:
            raise HTTPException(status_code=404, detail="Brigada no encontrada")
        return brigada
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/brigadas", response_model=str, status_code=201)
async def crear_brigada(
        brigada: BrigadaRequest,
        brigada_repo: BrigadaRepository = Depends(get_brigada_repository)
):
    """
    Crear una nueva brigada (con jefe y lista de trabajadores).
    """
    try:
        lider_ci = brigada.lider.CI
        integrantes_ci = [i.CI for i in brigada.integrantes]
        brigada_id = brigada_repo.create_brigada(lider_ci, integrantes_ci)
        return brigada_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/brigadas/{brigada_id}", response_model=bool)
async def editar_brigada(
        brigada_id: str,
        brigada: BrigadaRequest,
        brigada_repo: BrigadaRepository = Depends(get_brigada_repository)
):
    """
    Editar una brigada (actualizar jefe o trabajadores).
    """
    try:
        lider_ci = brigada.lider.CI
        integrantes_ci = [i.CI for i in brigada.integrantes]
        ok = brigada_repo.update_brigada(brigada_id, lider_ci, integrantes_ci)
        if not ok:
            raise HTTPException(status_code=404, detail="Brigada no encontrada o sin cambios")
        return ok
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/brigadas/{brigada_id}", response_model=bool)
async def eliminar_brigada(
        brigada_id: str,
        brigada_repo: BrigadaRepository = Depends(get_brigada_repository)
):
    """
    Eliminar una brigada.
    """
    try:
        ok = brigada_repo.delete_brigada(brigada_id)
        if not ok:
            raise HTTPException(status_code=404, detail="Brigada no encontrada")
        return ok
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Trabajadores en brigada ---

@router.post("/brigadas/{brigada_id}/trabajadores", response_model=bool)
async def agregar_trabajador(
        brigada_id: str,
        trabajador: TeamMember,
        brigada_repo: BrigadaRepository = Depends(get_brigada_repository)
):
    """
    Agregar un trabajador a una brigada existente.
    """
    try:
        ok = brigada_repo.add_trabajador(brigada_id, trabajador.CI)
        if not ok:
            raise HTTPException(status_code=404, detail="Brigada no encontrada o trabajador ya es integrante")
        return ok
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/brigadas/{brigada_id}/trabajadores/{trabajador_ci}", response_model=bool)
async def eliminar_trabajador(
        brigada_id: str,
        trabajador_ci: str,
        brigada_repo: BrigadaRepository = Depends(get_brigada_repository)
):
    """
    Eliminar un trabajador de una brigada.
    """
    try:
        ok = brigada_repo.remove_trabajador(brigada_id, trabajador_ci)
        if not ok:
            raise HTTPException(status_code=404, detail="Brigada o trabajador no encontrado")
        return ok
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/brigadas/{brigada_id}/trabajadores/{trabajador_ci}", response_model=bool)
async def editar_trabajador(
        brigada_id: str,
        trabajador_ci: str,
        trabajador: TeamMember,
        brigada_repo: BrigadaRepository = Depends(get_brigada_repository)
):
    """
    Editar los datos de un trabajador (nombre).
    """
    try:
        ok = brigada_repo.update_trabajador(trabajador_ci, trabajador.nombre)
        if not ok:
            raise HTTPException(status_code=404, detail="Trabajador no encontrado o sin cambios")
        return ok
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
