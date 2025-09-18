from typing import Optional
import json

from fastapi import APIRouter, Depends, HTTPException, Body, Path, UploadFile, File, Form
from pydantic import BaseModel

from application.services.oferta_service import OfertaService
from domain.entities.oferta import Oferta
from infrastucture.dependencies import get_oferta_service
from infrastucture.external_services.minio_uploader import upload_file_to_minio
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
    precio_cliente: Optional[float] = None
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
async def create_oferta(
    descripcion: str = Form(...),
    precio: float = Form(...),
    precio_cliente: Optional[float] = Form(None),
    garantias: str = Form(default="[]"),
    elementos: str = Form(default="[]"),
    imagen: Optional[UploadFile] = File(None),
    oferta_service: OfertaService = Depends(get_oferta_service)
):
    try:
        # Parse JSON fields
        garantias_list = json.loads(garantias)
        elementos_list = json.loads(elementos)

        # Upload image to MinIO if provided
        imagen_url = None
        if imagen:
            content = await imagen.read()
            imagen_url = await upload_file_to_minio(content, imagen.filename, imagen.content_type, "ofertas")

        # Create oferta data
        oferta_data = {
            "descripcion": descripcion,
            "precio": precio,
            "precio_cliente": precio_cliente,
            "imagen": imagen_url,
            "garantias": garantias_list,
            "elementos": elementos_list
        }

        oferta_id = await oferta_service.create(oferta_data)
        return OfertaCreateResponse(success=True, message="Oferta creada", oferta_id=oferta_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{oferta_id}", response_model=OfertaUpdateResponse)
async def update_oferta(
    oferta_id: str,
    descripcion: Optional[str] = Form(None),
    precio: Optional[float] = Form(None),
    precio_cliente: Optional[float] = Form(None),
    garantias: Optional[str] = Form(None),
    elementos: Optional[str] = Form(None),
    imagen: Optional[UploadFile] = File(None),
    oferta_service: OfertaService = Depends(get_oferta_service)
):
    try:
        new_data = {}

        # Only update fields that are provided
        if descripcion is not None:
            new_data["descripcion"] = descripcion
        if precio is not None:
            new_data["precio"] = precio
        if precio_cliente is not None:
            new_data["precio_cliente"] = precio_cliente
        if garantias is not None:
            new_data["garantias"] = json.loads(garantias)
        if elementos is not None:
            new_data["elementos"] = json.loads(elementos)

        # Upload new image if provided
        if imagen:
            content = await imagen.read()
            imagen_url = await upload_file_to_minio(content, imagen.filename, imagen.content_type, "ofertas")
            new_data["imagen"] = imagen_url

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


