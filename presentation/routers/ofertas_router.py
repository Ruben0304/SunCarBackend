from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Body, Path
from pydantic import BaseModel

from application.services.oferta_service import OfertaService
from domain.entities.oferta import Oferta
from infrastucture.dependencies import get_oferta_service
from presentation.schemas.responses.ofertas_responses import (
    OfertasListResponse,
    OfertaGetResponse,
    OfertaCreateResponse,
    OfertaUpdateResponse,
    OfertaDeleteResponse,
    OfertasSimplificadasListResponse
)


router = APIRouter()


class OfertaCreateRequest(BaseModel):
    descripcion: str
    precio: float
    imagen: Optional[str] = None
    garantias: list[str] = []
    elementos: list[dict] = []


@router.get("/simplified", response_model=OfertasSimplificadasListResponse)
async def read_ofertas_simplificadas(oferta_service: OfertaService = Depends(get_oferta_service)):
    try:
        data = await oferta_service.get_all_simplified()
        return OfertasSimplificadasListResponse(success=True, message="Ofertas simplificadas obtenidas", data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=OfertasListResponse)
async def read_ofertas(oferta_service: OfertaService = Depends(get_oferta_service)):
    try:
        data = await oferta_service.get_all()
        return OfertasListResponse(success=True, message="Ofertas obtenidas", data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{oferta_id}", response_model=OfertaGetResponse)
async def read_oferta_by_id(oferta_id: str, oferta_service: OfertaService = Depends(get_oferta_service)):
    try:
        data = await oferta_service.get_by_id(oferta_id)
        if not data:
            return OfertaGetResponse(success=False, message="Oferta no encontrada", data=None)
        return OfertaGetResponse(success=True, message="Oferta encontrada", data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=OfertaCreateResponse)
async def create_oferta(request: OfertaCreateRequest, oferta_service: OfertaService = Depends(get_oferta_service)):
    try:
        oferta_id = await oferta_service.create(request.model_dump())
        return OfertaCreateResponse(success=True, message="Oferta creada", oferta_id=oferta_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{oferta_id}", response_model=OfertaUpdateResponse)
async def update_oferta(
    oferta_id: str,
    new_data: dict = Body(..., description="Campos a actualizar de la oferta"),
    oferta_service: OfertaService = Depends(get_oferta_service)
):
    try:
        ok = await oferta_service.update(oferta_id, new_data)
        if not ok:
            return OfertaUpdateResponse(success=False, message="Oferta no encontrada o sin cambios")
        return OfertaUpdateResponse(success=True, message="Oferta actualizada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{oferta_id}", response_model=OfertaDeleteResponse)
async def delete_oferta(
    oferta_id: str = Path(..., description="ID de la oferta"),
    oferta_service: OfertaService = Depends(get_oferta_service)
):
    try:
        ok = await oferta_service.delete(oferta_id)
        if not ok:
            return OfertaDeleteResponse(success=False, message="Oferta no encontrada o no eliminada")
        return OfertaDeleteResponse(success=True, message="Oferta eliminada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


