from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime, date
import re


class TeamMember(BaseModel):
    """Modelo para miembro del equipo"""
    nombre: str = Field(..., min_length=1, description="Nombre del miembro del equipo")
    CI: str = Field(..., min_length=1, max_length=20, description="Cédula de identidad")

    @validator('nombre')
    def validate_nombre(cls, v):
        if not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip()

    @validator('CI')
    def validate_ci(cls, v):
        if not v.strip():
            raise ValueError('La CI no puede estar vacía')
        # Validación básica de CI (solo números y guiones)
        if not re.match(r'^[\d\-]+$', v.strip()):
            raise ValueError('La CI debe contener solo números y guiones')
        return v.strip()


class BrigadaRequest(BaseModel):
    """Datos de la brigada para el request"""
    lider: TeamMember = Field(..., description="Líder de la brigada")
    integrantes: List[TeamMember] = Field(..., min_items=0, description="Lista de integrantes de la brigada")

    @validator('integrantes')
    def validate_integrantes(cls, v):
        # Verificar que no haya CIs duplicadas en los integrantes
        cis = [miembro.CI for miembro in v]
        if len(cis) != len(set(cis)):
            raise ValueError('No puede haber integrantes con la misma CI')
        return v


class MaterialRequest(BaseModel):
    """Datos de materiales para el request"""
    tipo: str = Field(..., min_length=1, max_length=50, description="Tipo de material")
    nombre: str = Field(..., min_length=1, description="Nombre del material")
    cantidad: str = Field(..., min_length=1, description="Cantidad del material")
    unidad_medida: str = Field(..., min_length=1, max_length=20, description="Unidad de medida")
    codigo_producto: str = Field(..., min_length=1, description="Código del producto")

    @validator('cantidad')
    def validate_cantidad(cls, v):
        # Verificar que la cantidad sea un número válido
        try:
            float(v)
        except ValueError:
            raise ValueError('La cantidad debe ser un número válido')
        if float(v) <= 0:
            raise ValueError('La cantidad debe ser mayor a 0')
        return v

    @validator('tipo', 'nombre', 'unidad_medida', 'codigo_producto')
    def validate_string_fields(cls, v):
        if not v.strip():
            raise ValueError('Este campo no puede estar vacío')
        return v.strip()


class ClienteRequest(BaseModel):
    """Datos de cliente para el request"""
    numero: str = Field(..., min_length=1, max_length=200, description="Numero del cliente")

    @validator('numero')
    def validate_numero(cls, v):
        if not v.strip():
            raise ValueError('El numero de cliente no puede estar vacio')
        return v.strip()


class FechaHoraRequest(BaseModel):
    """Datos de fecha y hora para el request"""
    fecha: str = Field(..., description="Fecha en formato ISO (YYYY-MM-DD)")
    hora_inicio: str = Field(..., description="Hora de inicio en formato HH:MM")
    hora_fin: str = Field(..., description="Hora de fin en formato HH:MM")

    @validator('fecha')
    def validate_fecha(cls, v):
        try:
            # Validar formato de fecha ISO
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('El formato de fecha debe ser YYYY-MM-DD')
        return v

    @validator('hora_inicio', 'hora_fin')
    def validate_hora(cls, v):
        try:
            # Validar formato de hora HH:MM
            datetime.strptime(v, '%H:%M')
        except ValueError:
            raise ValueError('El formato de hora debe ser HH:MM')
        return v

    @validator('hora_fin')
    def validate_hora_fin(cls, v, values):
        if 'hora_inicio' in values:
            try:
                inicio = datetime.strptime(values['hora_inicio'], '%H:%M').time()
                fin = datetime.strptime(v, '%H:%M').time()
                if fin <= inicio:
                    raise ValueError('La hora de fin debe ser posterior a la hora de inicio')
            except ValueError as e:
                if "posterior" in str(e):
                    raise e
                # Si hay error de formato, se maneja en el validador individual
        return v


class AdjuntosRequest(BaseModel):
    """Datos de adjuntos para el request"""
    fotos_inicio: Optional[List[str]] = Field(default=[], description="Lista de URLs de fotos de inicio")
    fotos_fin: Optional[List[str]] = Field(default=[], description="Lista de URLs de fotos de fin")
    firma_cliente: Optional[str] = Field(None, description="URL de la firma del cliente")

    @validator('fotos_inicio', 'fotos_fin')
    def validate_fotos(cls, v):
        if v is None:
            return []
        for url in v:
            if not url.strip():
                raise ValueError('Las URLs de las fotos no pueden estar vacías')
        return v

    @validator('firma_cliente')
    def validate_firma_cliente(cls, v):
        if v is None:
            return v
        if not v.strip():
            raise ValueError('La URL de la firma del cliente no puede estar vacía')
        return v


class AveriaRequest(BaseModel):
    """Request schema para el reporte de avería"""
    tipo_reporte: str = Field(default="averia", description="Tipo de reporte")
    brigada: BrigadaRequest = Field(..., description="Datos de la brigada")
    materiales: Optional[List[MaterialRequest]] = Field(default=[], description="Lista de materiales (opcional)")
    cliente: ClienteRequest = Field(..., description="Datos de cliente")
    fecha_hora: FechaHoraRequest = Field(..., description="Datos de fecha y hora")
    descripcion: str = Field(..., min_length=1, max_length=1000, description="Descripción de la avería")
    adjuntos: AdjuntosRequest = Field(..., description="Archivos adjuntos")
    fecha_creacion: str = Field(default_factory=lambda: date.today().isoformat(),
                                description="Fecha de creación del reporte")

    @validator('tipo_reporte')
    def validate_tipo_reporte(cls, v):
        if v != "averia":
            raise ValueError('El tipo de reporte debe ser "averia"')
        return v

    @validator('descripcion')
    def validate_descripcion(cls, v):
        if not v.strip():
            raise ValueError('La descripción no puede estar vacía')
        return v.strip()

    class Config:
        # Configuración para mejor manejo de errores y documentación
        json_schema_extra = {
            "example": {
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
                    "numero": "1001"
                },
                "fecha_hora": {
                    "fecha": "2024-01-15",
                    "hora_inicio": "08:00",
                    "hora_fin": "17:00"
                },
                "descripcion": "Falla en el sistema eléctrico del cliente, se detectó un cortocircuito en el panel principal",
                "adjuntos": {
                    "fotos_inicio": ["base64_string_1"],
                    "fotos_fin": ["base64_string_2"]
                }
            }
        } 