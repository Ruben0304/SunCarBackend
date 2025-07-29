# PDF Use Cases

Esta carpeta contiene todos los casos de uso relacionados con la generación de PDFs en el sistema SunCar.

## Estructura

```
pdfUseCases/
├── __init__.py                 # Exporta todas las clases de casos de uso
├── base_pdf_use_case.py        # Clase base con funcionalidades comunes
├── generar_salarios_prueba.py  # Caso de uso para salarios de prueba
├── generar_salarios_reales.py  # Caso de uso para salarios reales
├── generar_inventario.py       # Caso de uso para inventario
└── README.md                   # Esta documentación
```

## Casos de Uso Disponibles

### 1. GenerarSalariosPruebaUseCase

- **Propósito**: Genera un PDF de prueba con datos de salarios predefinidos
- **Método**: `execute()`
- **Parámetros**: Ninguno
- **Retorna**: `bytes` (contenido del PDF)

### 2. GenerarSalariosRealesUseCase

- **Propósito**: Genera un PDF de salarios con datos reales de trabajadores
- **Método**: `execute(trabajadores)`
- **Parámetros**:
  - `trabajadores`: Lista de diccionarios con datos de trabajadores
- **Retorna**: `bytes` (contenido del PDF)

### 3. GenerarInventarioUseCase

- **Propósito**: Genera un PDF de inventario con datos de productos
- **Método**: `execute(productos)`
- **Parámetros**:
  - `productos`: Lista de diccionarios con datos de productos
- **Retorna**: `bytes` (contenido del PDF)

## Clase Base

### BasePDFUseCase

Proporciona funcionalidades comunes para todos los casos de uso:

- `_get_base_html_template()`: Retorna el template HTML base
- `_generate_pdf_from_html(html_content)`: Convierte HTML a PDF
- `_get_current_datetime()`: Retorna fecha y hora actual formateada
- `_format_currency(amount)`: Formatea números como moneda

## Cómo Agregar un Nuevo Caso de Uso

1. **Crear el archivo del caso de uso**:

   ```python
   from typing import List, Dict, Any
   from jinja2 import Template
   from .base_pdf_use_case import BasePDFUseCase

   class MiNuevoCasoDeUso(BasePDFUseCase):
       async def execute(self, datos: List[Dict[str, Any]]) -> bytes:
           # Tu lógica aquí
           pass
   ```

2. **Actualizar `__init__.py`**:

   ```python
   from .mi_nuevo_caso_de_uso import MiNuevoCasoDeUso

   __all__ = [
       # ... otros casos de uso
       'MiNuevoCasoDeUso'
   ]
   ```

3. **Actualizar el servicio PDF**:

   ```python
   from application.pdfUseCases import MiNuevoCasoDeUso

   class PDFService:
       async def mi_nuevo_metodo(self, datos):
           use_case = MiNuevoCasoDeUso()
           return await use_case.execute(datos)
   ```

## Ventajas de esta Estructura

1. **Separación de Responsabilidades**: Cada caso de uso tiene una responsabilidad específica
2. **Reutilización**: La clase base comparte funcionalidades comunes
3. **Mantenibilidad**: Es fácil modificar o agregar nuevos casos de uso
4. **Testabilidad**: Cada caso de uso puede ser probado independientemente
5. **Escalabilidad**: El código no se vuelve monolítico al crecer

## Ejemplo de Uso

```python
from application.pdfUseCases import GenerarSalariosRealesUseCase

# Crear instancia del caso de uso
use_case = GenerarSalariosRealesUseCase()

# Ejecutar el caso de uso
trabajadores = [
    {
        "nombre": "Juan Pérez",
        "ci": "12345678",
        "cargo": "Mecánico",
        "brigada": "Brigada A",
        "salario": "2500000"
    }
]

pdf_bytes = await use_case.execute(trabajadores)
```
