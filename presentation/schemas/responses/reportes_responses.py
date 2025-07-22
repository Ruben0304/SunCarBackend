from typing import Optional
from pydantic import BaseModel, Field


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
                    "cliente": {
                        "numero": "1001",
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


class AveriaReportResponse(BaseModel):
    """Respuesta del endpoint de reporte de avería"""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    message: str = Field(..., description="Mensaje descriptivo del resultado")
    data: Optional[dict] = Field(default=None, description="Datos del reporte recibido")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Reporte de avería recibido correctamente y validado",
                "data": {
                    "tipo_reporte": "averia",
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
                            "tipo": "Repuesto",
                            "nombre": "Fusible 10A",
                            "cantidad": "2",
                            "unidad_medida": "unidad",
                            "codigo_producto": "FUS001"
                        }
                    ],
                    "cliente": {
                        "numero": "1001",
                    },
                    "fecha_hora": {
                        "fecha": "2024-01-15",
                        "hora_inicio": "08:00",
                        "hora_fin": "17:00"
                    },
                    "descripcion": "Falla en el sistema eléctrico del cliente, se detectó un cortocircuito en el panel principal",
                    "adjuntos": {
                        "fotos_inicio": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."],
                        "fotos_fin": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."]
                    }
                }
            }
        }


class MantenimientoReportResponse(BaseModel):
    """Respuesta del endpoint de reporte de mantenimiento"""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    message: str = Field(..., description="Mensaje descriptivo del resultado")
    data: Optional[dict] = Field(default=None, description="Datos del reporte recibido")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Reporte de mantenimiento recibido correctamente y validado",
                "data": {
                    "tipo_reporte": "mantenimiento",
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
                            "tipo": "Lubricante",
                            "nombre": "Aceite sintético",
                            "cantidad": "1",
                            "unidad_medida": "litro",
                            "codigo_producto": "ACE001"
                        }
                    ],
                    "cliente": {
                        "numero": "1001",
                    },
                    "fecha_hora": {
                        "fecha": "2024-01-15",
                        "hora_inicio": "08:00",
                        "hora_fin": "17:00"
                    },
                    "descripcion": "Mantenimiento preventivo del sistema eléctrico, limpieza de contactos y verificación de conexiones",
                    "adjuntos": {
                        "fotos_inicio": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."],
                        "fotos_fin": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."]
                    }
                }
            }
        }


class HoursWorkedResponse(BaseModel):
    """Respuesta del endpoint de horas trabajadas por CI"""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    message: str = Field(..., description="Mensaje descriptivo del resultado")
    data: Optional[dict] = Field(default=None, description="Datos de las horas trabajadas")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Horas trabajadas obtenidas exitosamente",
                "data": {
                    "ci": "12345678",
                    "nombre": "Juan Pérez",
                    "fecha_inicio": "2024-01-01",
                    "fecha_fin": "2024-01-31",
                    "total_horas": 160.5,
                    "actividades": [
                        {
                            "fecha": "2024-01-15",
                            "hora_inicio": "08:00",
                            "hora_fin": "17:00",
                            "tipo_reporte": "inversion",
                            "horas_trabajadas": 9.0
                        }
                    ]
                }
            }
        }


class AllWorkersHoursWorkedResponse(BaseModel):
    """Respuesta del endpoint de horas trabajadas de todos los trabajadores"""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    message: str = Field(..., description="Mensaje descriptivo del resultado")
    data: Optional[dict] = Field(default=None, description="Datos de las horas trabajadas de todos los trabajadores")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Horas trabajadas de todos los trabajadores obtenidas exitosamente",
                "data": {
                    "fecha_inicio": "2024-01-01",
                    "fecha_fin": "2024-01-31",
                    "total_trabajadores": 5,
                    "trabajadores": [
                        {
                            "ci": "12345678",
                            "nombre": "Juan",
                            "apellido": "Pérez",
                            "total_horas": 160.5
                        },
                        {
                            "ci": "87654321",
                            "nombre": "María",
                            "apellido": "García",
                            "total_horas": 145.0
                        },
                        {
                            "ci": "11223344",
                            "nombre": "Carlos",
                            "apellido": "López",
                            "total_horas": 132.75
                        }
                    ]
                }
            }
        } 

class MaterialUsadoResponse(BaseModel):
    codigo: str
    descripcion: str
    um: str
    cantidad: float

class MaterialesPorBrigadaResponse(BaseModel):
    lider_ci: str
    lider_nombre: str
    materiales: list[MaterialUsadoResponse]

class MaterialesUsadosBrigadaResponse(BaseModel):
    success: bool
    message: str
    materiales: list[MaterialUsadoResponse]

class MaterialesUsadosTodasBrigadasResponse(BaseModel):
    success: bool
    message: str
    brigadas: list[MaterialesPorBrigadaResponse] 