from http.client import HTTPException
from typing import List, Optional

from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile, Form
from pydantic import BaseModel, Field, ValidationError

from presentation.schemas.requests.InversionFormRequest import InversionRequest
from application.services.form_service import FormService
from infrastucture.repositories.formularios_repository import FormRepository
from infrastucture.external_services.base64_file_converter import FileBase64Converter
import base64
import json

router = APIRouter()

form_service = FormService(FormRepository())


class InversionReportResponse(BaseModel):
    """Respuesta del endpoint de reporte de inversión"""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    message: str = Field(..., description="Mensaje descriptivo del resultado")
    data: Optional[dict] = Field(default=None, description="Datos del reporte recibido")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Reporte de inversión recibido correctamente y validado",
                "data": {
                    "tipo_reporte": "inversion",
                    "brigada": {
                        "lider": {
                            "nombre": "Juan Pérez",
                            "CI": "12345678"
                        },
                        "integrantes": [
                            {
                                "nombre": "María García",
                                "CI": "87654321"
                            }
                        ]
                    },
                    "materiales": [
                        {
                            "tipo": "Cemento",
                            "nombre": "Cemento Portland",
                            "cantidad": "10",
                            "unidad_medida": "kg",
                            "codigo_producto": "CEM001"
                        }
                    ],
                    "ubicacion": {
                        "direccion": "Av. Principal 123",
                        "latitud": "-17.3895",
                        "longitud": "-66.1568"
                    },
                    "fecha_hora": {
                        "fecha": "2024-01-15",
                        "hora_inicio": "08:00",
                        "hora_fin": "17:00"
                    },
                    "adjuntos": {
                        "fotos_inicio": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."],
                        "fotos_fin": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."]
                    }
                }
            }
        }


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
    ubicacion: str = Form(...),
    fecha_hora: str = Form(...),
    fotos_inicio: list[UploadFile] = File(...),
    fotos_fin: list[UploadFile] = File(...)
):
    """
    Crea un nuevo reporte de inversión en el sistema.
    
    ## Funcionalidades:
    - ✅ Validación automática de todos los campos
    - ✅ Verificación de formatos de fecha y hora
    - ✅ Validación de coordenadas geográficas
    - ✅ Verificación de CIs únicas en la brigada
    - ✅ Validación de imágenes en formato base64
    
    ## Campos Requeridos:
    - **brigada**: Información del líder y equipo de trabajo
    - **materiales**: Lista de materiales utilizados (mínimo 1)
    - **ubicacion**: Dirección y coordenadas del trabajo
    - **fecha_hora**: Programación temporal del trabajo
    - **adjuntos**: Fotos del antes y después
    
    ## Validaciones:
    - Las CIs de los integrantes deben ser únicas
    - La hora de fin debe ser posterior a la hora de inicio
    - Las coordenadas deben estar en rangos válidos
    - Las cantidades de materiales deben ser números positivos
    - Debe incluir al menos una foto de inicio y fin
    """
    try:
        # Parsear los campos JSON
        brigada_dict = json.loads(brigada)
        materiales_list = json.loads(materiales)
        ubicacion_dict = json.loads(ubicacion)
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
            "ubicacion": ubicacion_dict,
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