from http.client import HTTPException
from typing import List, Optional

from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile, Form, Query
from pydantic import BaseModel, Field, ValidationError

from infrastucture.dependencies import get_form_service
from presentation.schemas.requests.InversionFormRequest import InversionRequest
from presentation.schemas.requests.AveriaFormRequest import AveriaRequest
from presentation.schemas.requests.MantenimientoFormRequest import MantenimientoRequest
from application.services.form_service import FormService
from infrastucture.repositories.reportes_repository import FormRepository
from infrastucture.external_services.base64_file_converter import FileBase64Converter
from presentation.schemas.responses import (
    InversionReportResponse,
    AveriaReportResponse,
    MantenimientoReportResponse,
)
from domain.entities.form import Form as FormEntity
import base64
import json

router = APIRouter()



# @router.get("/", response_model=List[FormEntity])
# async def get_all_forms() -> List[FormEntity]:
#     forms = await form_service.get_all_forms()
#     return forms


@router.post(
    "/inversion",
    response_model=InversionReportResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear Reporte de Inversión",
    description="""
    Endpoint para crear un nuevo reporte de inversión.
    
    Este endpoint recibe los datos completos de un reporte de inversión incluyendo:
    - **Brigada**: Información del líder y integrantes del equipo
    - **Materiales**: Lista de materiales utilizados en el trabajo
    - **Ubicación**: Dirección y coordenadas geográficas del trabajo
    - **Fecha y Hora**: Programación temporal del trabajo
    - **Adjuntos**: Fotos del antes y después del trabajo
    
    El sistema validará automáticamente todos los datos según las reglas de negocio definidas.
    """,
    response_description="Reporte de inversión creado exitosamente",
    tags=["Reportes de Inversión"]
)
async def create_inversion_report(
        tipo_reporte: str = Form(...),
        brigada: str = Form(...),
        materiales: str = Form(...),
        cliente: str = Form(...),
        fecha_hora: str = Form(...),
        fotos_inicio: list[UploadFile] = File(...),
        fotos_fin: list[UploadFile] = File(...),
        firma_cliente: UploadFile = File(None),
        form_service: FormService = Depends(get_form_service)
):
    try:
        # Parsear los campos JSON
        brigada_dict = json.loads(brigada)
        materiales_list = json.loads(materiales)
        cliente_dict = json.loads(cliente)
        fecha_hora_dict = json.loads(fecha_hora)

        fotos_inicio_base64 = await FileBase64Converter.files_to_base64(fotos_inicio)
        fotos_fin_base64 = await FileBase64Converter.files_to_base64(fotos_fin)
        adjuntos = {
            "fotos_inicio": fotos_inicio_base64,
            "fotos_fin": fotos_fin_base64
        }
        if firma_cliente:
            firma_cliente_base64 = (await FileBase64Converter.files_to_base64([firma_cliente]))[0]
            adjuntos["firma_cliente"] = firma_cliente_base64

        request_data = {
            "tipo_reporte": tipo_reporte,
            "brigada": brigada_dict,
            "materiales": materiales_list,
            "cliente": cliente_dict,
            "fecha_hora": fecha_hora_dict,
            "adjuntos": adjuntos
        }

        inversion_request = InversionRequest(**request_data)
        form_id = form_service.save_form(inversion_request.dict())
        return InversionReportResponse(
            success=True,
            message=f"Reporte de inversión recibido y guardado con id {form_id}",
            data=inversion_request.dict()
        )
    except ValidationError as e:
        error_messages = []
        for error in e.errors():
            field_path = " -> ".join(str(loc) for loc in error['loc'])
            error_msg = f"{field_path}: {error['msg']}"
            error_messages.append(error_msg)
        error_summary = "; ".join(error_messages)
        return InversionReportResponse(
            success=False,
            message=f"Errores de validación detectados: {error_summary}",
            data={}
        )
    except Exception as e:
        return InversionReportResponse(
            success=False,
            message=f"Error interno del servidor: {str(e)}",
            data={}
        )


@router.post(
    "/averia",
    response_model=AveriaReportResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear Reporte de Avería",
    description="""
    Endpoint para crear un nuevo reporte de avería.
    
    Este endpoint recibe los datos completos de un reporte de avería incluyendo:
    - **Brigada**: Información del líder y integrantes del equipo
    - **Materiales**: Lista de materiales utilizados en el trabajo (opcional)
    - **Cliente**: Información del cliente
    - **Fecha y Hora**: Programación temporal del trabajo
    - **Descripción**: Descripción detallada de la avería
    - **Adjuntos**: Fotos del antes y después del trabajo (opcional)
    
    El sistema validará automáticamente todos los datos según las reglas de negocio definidas.
    """,
    response_description="Reporte de avería creado exitosamente",
    tags=["Reportes de Avería"]
)
async def create_averia_report(
        tipo_reporte: str = Form(...),
        brigada: str = Form(...),
        materiales: str = Form(default="[]"),
        cliente: str = Form(...),
        fecha_hora: str = Form(...),
        descripcion: str = Form(...),
        fotos_inicio: list[UploadFile] = File(default=[]),
        fotos_fin: list[UploadFile] = File(default=[]),
        form_service: FormService = Depends(get_form_service)
):
    try:
        # Parsear los campos JSON
        brigada_dict = json.loads(brigada)
        materiales_list = json.loads(materiales)
        cliente_dict = json.loads(cliente)
        fecha_hora_dict = json.loads(fecha_hora)

        # Procesar fotos solo si se proporcionan
        fotos_inicio_base64 = []
        fotos_fin_base64 = []

        if fotos_inicio:
            fotos_inicio_base64 = await FileBase64Converter.files_to_base64(fotos_inicio)
        if fotos_fin:
            fotos_fin_base64 = await FileBase64Converter.files_to_base64(fotos_fin)

        adjuntos = {
            "fotos_inicio": fotos_inicio_base64,
            "fotos_fin": fotos_fin_base64
        }

        request_data = {
            "tipo_reporte": tipo_reporte,
            "brigada": brigada_dict,
            "materiales": materiales_list,
            "cliente": cliente_dict,
            "fecha_hora": fecha_hora_dict,
            "descripcion": descripcion,
            "adjuntos": adjuntos
        }

        averia_request = AveriaRequest(**request_data)
        form_id = form_service.save_form(averia_request.dict())
        return AveriaReportResponse(
            success=True,
            message=f"Reporte de avería recibido y guardado con id {form_id}",
            data=averia_request.dict()
        )
    except ValidationError as e:
        error_messages = []
        for error in e.errors():
            field_path = " -> ".join(str(loc) for loc in error['loc'])
            error_msg = f"{field_path}: {error['msg']}"
            error_messages.append(error_msg)
        error_summary = "; ".join(error_messages)
        return AveriaReportResponse(
            success=False,
            message=f"Errores de validación detectados: {error_summary}",
            data={}
        )
    except Exception as e:
        return AveriaReportResponse(
            success=False,
            message=f"Error interno del servidor: {str(e)}",
            data={}
        )


@router.post(
    "/mantenimiento",
    response_model=MantenimientoReportResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear Reporte de Mantenimiento",
    description="""
    Endpoint para crear un nuevo reporte de mantenimiento.
    
    Este endpoint recibe los datos completos de un reporte de mantenimiento incluyendo:
    - **Brigada**: Información del líder y integrantes del equipo
    - **Materiales**: Lista de materiales utilizados en el trabajo (opcional)
    - **Cliente**: Información del cliente
    - **Fecha y Hora**: Programación temporal del trabajo
    - **Descripción**: Descripción detallada del mantenimiento realizado
    - **Adjuntos**: Fotos del antes y después del trabajo (opcional)
    
    El sistema validará automáticamente todos los datos según las reglas de negocio definidas.
    """,
    response_description="Reporte de mantenimiento creado exitosamente",
    tags=["Reportes de Mantenimiento"]
)
async def create_mantenimiento_report(
        tipo_reporte: str = Form(...),
        brigada: str = Form(...),
        materiales: str = Form(default="[]"),
        cliente: str = Form(...),
        fecha_hora: str = Form(...),
        descripcion: str = Form(...),
        fotos_inicio: list[UploadFile] = File(default=[]),
        fotos_fin: list[UploadFile] = File(default=[]),
        form_service: FormService = Depends(get_form_service)
):
    try:
        # Parsear los campos JSON
        brigada_dict = json.loads(brigada)
        materiales_list = json.loads(materiales)
        cliente_dict = json.loads(cliente)
        fecha_hora_dict = json.loads(fecha_hora)

        # Procesar fotos solo si se proporcionan
        fotos_inicio_base64 = []
        fotos_fin_base64 = []

        if fotos_inicio:
            fotos_inicio_base64 = await FileBase64Converter.files_to_base64(fotos_inicio)
        if fotos_fin:
            fotos_fin_base64 = await FileBase64Converter.files_to_base64(fotos_fin)

        adjuntos = {
            "fotos_inicio": fotos_inicio_base64,
            "fotos_fin": fotos_fin_base64
        }

        request_data = {
            "tipo_reporte": tipo_reporte,
            "brigada": brigada_dict,
            "materiales": materiales_list,
            "cliente": cliente_dict,
            "fecha_hora": fecha_hora_dict,
            "descripcion": descripcion,
            "adjuntos": adjuntos
        }

        mantenimiento_request = MantenimientoRequest(**request_data)
        form_id = form_service.save_form(mantenimiento_request.dict())
        return MantenimientoReportResponse(
            success=True,
            message=f"Reporte de mantenimiento recibido y guardado con id {form_id}",
            data=mantenimiento_request.dict()
        )
    except ValidationError as e:
        error_messages = []
        for error in e.errors():
            field_path = " -> ".join(str(loc) for loc in error['loc'])
            error_msg = f"{field_path}: {error['msg']}"
            error_messages.append(error_msg)
        error_summary = "; ".join(error_messages)
        return MantenimientoReportResponse(
            success=False,
            message=f"Errores de validación detectados: {error_summary}",
            data={}
        )
    except Exception as e:
        return MantenimientoReportResponse(
            success=False,
            message=f"Error interno del servidor: {str(e)}",
            data={}
        )





@router.get("/", summary="Listar reportes", tags=["Reportes"], response_model=List[dict])
def listar_reportes(
    tipo_reporte: Optional[str] = Query(None, description="Tipo de reporte (inversion, averia, mantenimiento)"),
    cliente_numero: Optional[str] = Query(None, description="Número de cliente"),
    fecha_inicio: Optional[str] = Query(None, description="Fecha inicio (YYYY-MM-DD)"),
    fecha_fin: Optional[str] = Query(None, description="Fecha fin (YYYY-MM-DD)"),
    lider_ci: Optional[str] = Query(None, description="CI del líder de brigada"),
    descripcion: Optional[str] = Query(None, description="Búsqueda parcial en la descripción del reporte"),
    q: Optional[str] = Query(None, description="Búsqueda global en varios campos: descripción, nombre de cliente, nombre de líder, tipo de reporte, número de cliente"),
    form_service: FormService = Depends(get_form_service)
):
    """Listar reportes de la colección principal con filtros opcionales, incluyendo búsqueda global por 'q'."""
    reportes = form_service.get_reportes_view(tipo_reporte, cliente_numero, fecha_inicio, fecha_fin, lider_ci)
    return reportes


@router.get("/view", summary="Listar reportes desde la vista", tags=["Reportes"], response_model=List[dict])
def listar_reportes_view(
    tipo_reporte: Optional[str] = Query(None, description="Tipo de reporte (inversion, averia, mantenimiento)"),
    cliente_numero: Optional[str] = Query(None, description="Número de cliente"),
    fecha_inicio: Optional[str] = Query(None, description="Fecha inicio (YYYY-MM-DD)"),
    fecha_fin: Optional[str] = Query(None, description="Fecha fin (YYYY-MM-DD)"),
    lider_ci: Optional[str] = Query(None, description="CI del líder de brigada"),
    form_service: FormService = Depends(get_form_service)
):
    """Listar reportes desde la vista reportes_view con filtros opcionales."""
    reportes = form_service.get_reportes_view(tipo_reporte, cliente_numero, fecha_inicio, fecha_fin, lider_ci)
    return reportes


@router.get("/cliente/{numero}", summary="Listar reportes de un cliente", tags=["Reportes"], response_model=List[dict])
def listar_reportes_por_cliente(
    numero: str,
    desde_vista: Optional[bool] = Query(False, description="Si es True, consulta la vista reportes_view"),
    tipo_reporte: Optional[str] = Query(None, description="Filtrar por tipo de reporte (opcional)"),
    fecha_inicio: Optional[str] = Query(None, description="Fecha inicio (YYYY-MM-DD)"),
    fecha_fin: Optional[str] = Query(None, description="Fecha fin (YYYY-MM-DD)"),
    lider_ci: Optional[str] = Query(None, description="CI del líder de brigada (opcional)"),
    form_service: FormService = Depends(get_form_service)
):
    """Listar todos los reportes de un cliente (de cualquier tipo)."""
    if desde_vista:
        reportes = form_service.get_reportes_view(tipo_reporte, numero, fecha_inicio, fecha_fin, lider_ci)
    else:
        reportes = form_service.get_reportes(tipo_reporte, numero, fecha_inicio, fecha_fin, lider_ci, None, None)
    return reportes


@router.get("/{reporte_id}", summary="Obtener reporte por ID", tags=["Reportes"], response_model=dict)
def obtener_reporte_por_id(
    reporte_id: str,
    form_service: FormService = Depends(get_form_service)
):
    """Obtener los datos de un reporte por su ID."""
    reporte = form_service.get_reporte_by_id(reporte_id)
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return reporte
