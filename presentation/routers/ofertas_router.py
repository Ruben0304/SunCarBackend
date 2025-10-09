from typing import Optional, List
import json

from fastapi import APIRouter, Depends, HTTPException, Body, Path, UploadFile, File, Form
from pydantic import BaseModel

from application.services.oferta_service import OfertaService
from application.services.chat_service import ChatService
from domain.entities.oferta import Oferta, OfertaElemento
from infrastucture.dependencies import get_oferta_service, get_chat_service
from infrastucture.external_services.minio_uploader import upload_file_to_minio
from presentation.schemas.responses.ofertas_responses import (
    OfertasListResponse,
    OfertaGetResponse,
    OfertaCreateResponse,
    OfertaUpdateResponse,
    OfertaDeleteResponse,
    OfertasSimplificadasListResponse,
    ElementoAddResponse,
    ElementoDeleteResponse,
    ElementoUpdateResponse
)


router = APIRouter()




class OfertaCreateRequest(BaseModel):
    descripcion: str
    precio: float
    precio_cliente: Optional[float] = None
    garantias: list[str] = []
    elementos: list[dict] = []


class RecomendacionRequest(BaseModel):
    texto: str


class RecomendacionResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None


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
    descripcion_detallada: Optional[str] = Form(None),
    precio_cliente: Optional[float] = Form(None),
    moneda: Optional[str] = Form(None),
    financiamiento: Optional[bool] = Form(None),
    descuentos: Optional[str] = Form(None),
    garantias: str = Form(default="[]"),
    imagen: Optional[UploadFile] = File(None),
    oferta_service: OfertaService = Depends(get_oferta_service)
):
    try:
        # Parse JSON fields
        garantias_list = json.loads(garantias)

        # Upload image to MinIO if provided
        imagen_url = None
        if imagen:
            content = await imagen.read()
            imagen_url = await upload_file_to_minio(content, imagen.filename, imagen.content_type, "ofertas")

        # Create oferta data (sin elementos)
        oferta_data = {
            "descripcion": descripcion,
            "precio": precio,
            "precio_cliente": precio_cliente,
            "imagen": imagen_url,
            "garantias": garantias_list,
            "elementos": []
        }

        # Add optional fields only if provided
        if descripcion_detallada is not None:
            oferta_data["descripcion_detallada"] = descripcion_detallada
        if moneda is not None:
            oferta_data["moneda"] = moneda
        if financiamiento is not None:
            oferta_data["financiamiento"] = financiamiento
        if descuentos is not None:
            oferta_data["descuentos"] = descuentos

        oferta_id = await oferta_service.create(oferta_data)
        return OfertaCreateResponse(success=True, message="Oferta creada", oferta_id=oferta_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{oferta_id}", response_model=OfertaUpdateResponse)
async def update_oferta(
    oferta_id: str,
    descripcion: Optional[str] = Form(None),
    descripcion_detallada: Optional[str] = Form(None),
    precio: Optional[float] = Form(None),
    precio_cliente: Optional[float] = Form(None),
    moneda: Optional[str] = Form(None),
    financiamiento: Optional[bool] = Form(None),
    descuentos: Optional[str] = Form(None),
    garantias: Optional[str] = Form(None),
    imagen: Optional[UploadFile] = File(None),
    oferta_service: OfertaService = Depends(get_oferta_service)
):
    try:
        new_data = {}

        # Only update fields that are provided
        if descripcion is not None:
            new_data["descripcion"] = descripcion
        if descripcion_detallada is not None:
            new_data["descripcion_detallada"] = descripcion_detallada
        if precio is not None:
            new_data["precio"] = precio
        if precio_cliente is not None:
            new_data["precio_cliente"] = precio_cliente
        if moneda is not None:
            new_data["moneda"] = moneda
        if financiamiento is not None:
            new_data["financiamiento"] = financiamiento
        if descuentos is not None:
            new_data["descuentos"] = descuentos
        if garantias is not None:
            new_data["garantias"] = json.loads(garantias)

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


@router.post("/{oferta_id}/elementos", response_model=ElementoAddResponse)
async def add_elemento_to_oferta(
    oferta_id: str = Path(..., description="ID de la oferta"),
    categoria: str = Form(..., description="Categoría del elemento"),
    cantidad: float = Form(..., description="Cantidad del elemento (mayor a 0)"),
    descripcion: Optional[str] = Form(None, description="Descripción del elemento"),
    foto: Optional[UploadFile] = File(None, description="Foto del elemento"),
    oferta_service: OfertaService = Depends(get_oferta_service)
):
    try:
        # Validar cantidad
        if cantidad <= 0:
            raise HTTPException(status_code=400, detail="La cantidad debe ser mayor a 0")

        # Subir foto si existe
        foto_url = None
        if foto:
            content = await foto.read()
            foto_url = await upload_file_to_minio(content, foto.filename, foto.content_type, "ofertas")

        # Crear datos del elemento
        elemento_data = {
            "categoria": categoria,
            "descripcion": descripcion,
            "cantidad": cantidad,
            "foto": foto_url
        }

        ok = await oferta_service.add_elemento(oferta_id, elemento_data)
        if not ok:
            return ElementoAddResponse(success=False, message="Oferta no encontrada")
        return ElementoAddResponse(success=True, message="Elemento agregado a la oferta")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{oferta_id}/elementos/{elemento_index}", response_model=ElementoUpdateResponse)
async def update_elemento_from_oferta(
    oferta_id: str = Path(..., description="ID de la oferta"),
    elemento_index: int = Path(..., description="Índice del elemento a actualizar"),
    categoria: Optional[str] = Form(None, description="Nueva categoría del elemento"),
    cantidad: Optional[float] = Form(None, description="Nueva cantidad del elemento (mayor a 0)"),
    descripcion: Optional[str] = Form(None, description="Nueva descripción del elemento"),
    foto: Optional[UploadFile] = File(None, description="Nueva foto del elemento"),
    oferta_service: OfertaService = Depends(get_oferta_service)
):
    try:
        # Validar que al menos un campo se está actualizando
        if all(v is None for v in [categoria, cantidad, descripcion, foto]):
            raise HTTPException(status_code=400, detail="Debe proporcionar al menos un campo para actualizar")

        # Validar cantidad si se proporciona
        if cantidad is not None and cantidad <= 0:
            raise HTTPException(status_code=400, detail="La cantidad debe ser mayor a 0")

        # Subir nueva foto si se proporciona
        foto_url = None
        if foto:
            content = await foto.read()
            foto_url = await upload_file_to_minio(content, foto.filename, foto.content_type, "ofertas")

        # Crear datos de actualización solo con campos proporcionados
        nuevos_datos = {}
        if categoria is not None:
            nuevos_datos["categoria"] = categoria
        if cantidad is not None:
            nuevos_datos["cantidad"] = cantidad
        if descripcion is not None:
            nuevos_datos["descripcion"] = descripcion
        if foto_url is not None:
            nuevos_datos["foto"] = foto_url

        ok = await oferta_service.update_elemento(oferta_id, elemento_index, nuevos_datos)
        if not ok:
            return ElementoUpdateResponse(success=False, message="Oferta no encontrada o índice inválido")
        return ElementoUpdateResponse(success=True, message="Elemento actualizado en la oferta")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{oferta_id}/elementos/{elemento_index}", response_model=ElementoDeleteResponse)
async def delete_elemento_from_oferta(
    oferta_id: str = Path(..., description="ID de la oferta"),
    elemento_index: int = Path(..., description="Índice del elemento a eliminar"),
    oferta_service: OfertaService = Depends(get_oferta_service)
):
    try:
        ok = await oferta_service.remove_elemento(oferta_id, elemento_index)
        if not ok:
            return ElementoDeleteResponse(success=False, message="Oferta no encontrada o índice inválido")
        return ElementoDeleteResponse(success=True, message="Elemento eliminado de la oferta")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recomendador", response_model=RecomendacionResponse)
async def recomendar_ofertas(
    request: RecomendacionRequest = Body(...),
    oferta_service: OfertaService = Depends(get_oferta_service),
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    Sistema recomendador de ofertas basado en IA.
    Recibe texto del usuario y retorna todas las ofertas ordenadas por recomendación.
    """
    try:
        # 1. Obtener datos mínimos de todas las ofertas
        datos_minimos = await oferta_service.obtener_datos_minimos()

        if not datos_minimos:
            return RecomendacionResponse(
                success=False,
                message="No hay ofertas disponibles para recomendar"
            )

        # 2. Llamar al chat service para obtener recomendaciones
        resultado_ia = await chat_service.recomendar_ofertas(
            texto_usuario=request.texto,
            ofertas_contexto=datos_minimos
        )

        # 3. Obtener ofertas completas en formato simplificado usando los IDs ordenados
        ids_ordenados = resultado_ia.ids_ordenados
        ofertas_simplificadas = await oferta_service.obtener_ofertas_por_ids(ids_ordenados)

        # 4. Preparar respuesta final
        respuesta_final = {
            "texto": resultado_ia.texto,
            "ofertas": [oferta.model_dump() for oferta in ofertas_simplificadas]
        }

        return RecomendacionResponse(
            success=True,
            message="Recomendaciones generadas exitosamente",
            data=respuesta_final
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar recomendaciones: {str(e)}")


