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
    HoursWorkedResponse,
)
from domain.entities.form import Form as FormEntity
import base64
import json

from presentation.schemas.responses.reportes_responses import AllWorkersHoursWorkedResponse

router = APIRouter()

form_service = Depends(get_form_service)



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
        fotos_fin: list[UploadFile] = File(...)
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
        fotos_fin: list[UploadFile] = File(default=[])
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
        fotos_fin: list[UploadFile] = File(default=[])
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


@router.get(
    "/horas-trabajadas/{ci}",
    response_model=HoursWorkedResponse,
    status_code=status.HTTP_200_OK,
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
    tags=["Reportes - Consultas"]
)
async def get_hours_worked_by_ci(
    ci: str,
    fecha_inicio: str,
    fecha_fin: str
):
    try:
        total_horas = form_service.get_hours_worked_by_ci(ci, fecha_inicio, fecha_fin)
        
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
    status_code=status.HTTP_200_OK,
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
    tags=["Reportes - Consultas"]
)
async def get_all_workers_hours_worked(
    fecha_inicio: str,
    fecha_fin: str
):
    try:
        trabajadores = form_service.get_all_workers_hours_worked(fecha_inicio, fecha_fin)
        
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


@router.get("/", summary="Listar reportes", tags=["Reportes"], response_model=List[dict])
def listar_reportes(
    tipo_reporte: Optional[str] = Query(None, description="Tipo de reporte (inversion, averia, mantenimiento)"),
    cliente_numero: Optional[str] = Query(None, description="Número de cliente"),
    fecha_inicio: Optional[str] = Query(None, description="Fecha inicio (YYYY-MM-DD)"),
    fecha_fin: Optional[str] = Query(None, description="Fecha fin (YYYY-MM-DD)"),
    lider_ci: Optional[str] = Query(None, description="CI del líder de brigada"),
    descripcion: Optional[str] = Query(None, description="Búsqueda parcial en la descripción del reporte"),
    q: Optional[str] = Query(None, description="Búsqueda global en varios campos: descripción, nombre de cliente, nombre de líder, tipo de reporte, número de cliente"),
):
    """Listar reportes de la colección principal con filtros opcionales, incluyendo búsqueda global por 'q'."""
    reportes = form_service.get_reportes(tipo_reporte, cliente_numero, fecha_inicio, fecha_fin, lider_ci, descripcion, q)
    return reportes


@router.get("/view", summary="Listar reportes desde la vista", tags=["Reportes"], response_model=List[dict])
def listar_reportes_view(
    tipo_reporte: Optional[str] = Query(None, description="Tipo de reporte (inversion, averia, mantenimiento)"),
    cliente_numero: Optional[str] = Query(None, description="Número de cliente"),
    fecha_inicio: Optional[str] = Query(None, description="Fecha inicio (YYYY-MM-DD)"),
    fecha_fin: Optional[str] = Query(None, description="Fecha fin (YYYY-MM-DD)"),
    lider_ci: Optional[str] = Query(None, description="CI del líder de brigada"),
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
):
    """Listar todos los reportes de un cliente (de cualquier tipo)."""
    if desde_vista:
        reportes = form_service.get_reportes_view(tipo_reporte, numero, fecha_inicio, fecha_fin, lider_ci)
    else:
        reportes = form_service.get_reportes(tipo_reporte, numero, fecha_inicio, fecha_fin, lider_ci)
    return reportes
