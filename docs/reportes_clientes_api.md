# API de Reportes y Clientes

Esta documentación describe cómo crear reportes (inversión, avería, mantenimiento) y clientes, y cómo se relacionan entre sí. Está orientada a desarrolladores frontend.

---

## 1. Crear Cliente

### Endpoint
- **POST** `/api/clientes/`
- **Tipo de contenido:** `application/json`

### Descripción
Crea un nuevo cliente con información completa. Si el cliente ya existe (por número), lo actualiza.

### Campos requeridos (ejemplo):
```json
{
  "nombre": "Empresa X",
  "numero": "789",
  "direccion": "Calle 123",
  "latitud": "-12.3456",
  "longitud": "-65.4321"
}
```

### Respuesta exitosa
```json
{
  "success": true,
  "message": "Cliente creado exitosamente",
  "data": {
    "nombre": "Empresa X",
    "numero": "789",
    "direccion": "Calle 123",
    "latitud": "-12.3456",
    "longitud": "-65.4321"
  }
}
```

---

## 2. Crear Reporte de Inversión

### Endpoint
- **POST** `/api/reportes/inversion`
- **Tipo de contenido:** `multipart/form-data`

### Descripción
Crea un nuevo reporte de inversión. El cliente puede ser creado en el mismo momento del reporte (no es obligatorio que exista previamente).

### Campos requeridos
| Campo         | Tipo         | Descripción                                                                 |
|---------------|--------------|-----------------------------------------------------------------------------|
| tipo_reporte  | string       | Debe ser `"inversion"`                                                      |
| brigada       | string (JSON)| Información de la brigada (líder e integrantes)                             |
| materiales    | string (JSON)| Lista de materiales utilizados                                              |
| cliente       | string (JSON)| Información del cliente                                                     |
| fecha_hora    | string (JSON)| Información de fecha y hora del trabajo                                     |
| fotos_inicio  | archivo[]    | Fotos del inicio del trabajo (pueden ser varias)                            |
| fotos_fin     | archivo[]    | Fotos del final del trabajo (pueden ser varias)                             |

#### Ejemplo de request (Postman):
- **tipo_reporte:** `"inversion"`
- **brigada:** `{"lider": {"CI": "123", "nombre": "Juan"}, "integrantes": [{"CI": "456", "nombre": "Pedro"}]}`
- **materiales:** `[{"nombre": "Cemento", "cantidad": 5}]`
- **cliente:** `{"nombre": "Empresa X", "numero": "789"}`
- **fecha_hora:** `{"fecha": "2024-06-01", "hora": "10:00"}`
- **fotos_inicio:** (adjuntar archivos)
- **fotos_fin:** (adjuntar archivos)

#### Respuesta exitosa
```json
{
  "success": true,
  "message": "Reporte de inversión recibido y guardado con id 12345",
  "data": { ... }
}
```

#### Nota lógica
- **El cliente puede ser creado junto con el reporte de inversión.** Si el cliente no existe, se debe enviar toda la información en el campo `cliente`.

---

## 3. Crear Reporte de Avería

### Endpoint
- **POST** `/api/reportes/averia`
- **Tipo de contenido:** `multipart/form-data`

### Descripción
Crea un nuevo reporte de avería. El cliente **debe existir previamente**; se asocia por su información.

### Campos requeridos
| Campo         | Tipo         | Descripción                                                                 |
|---------------|--------------|-----------------------------------------------------------------------------|
| tipo_reporte  | string       | Debe ser `"averia"`                                                         |
| brigada       | string (JSON)| Información de la brigada                                                   |
| materiales    | string (JSON)| Lista de materiales utilizados (opcional, puede ser `"[]"`)                 |
| cliente       | string (JSON)| Información del cliente                                                     |
| fecha_hora    | string (JSON)| Información de fecha y hora del trabajo                                     |
| descripcion   | string       | Descripción detallada de la avería                                          |
| fotos_inicio  | archivo[]    | Fotos del inicio del trabajo (opcional)                                     |
| fotos_fin     | archivo[]    | Fotos del final del trabajo (opcional)                                      |

#### Ejemplo de request
- **tipo_reporte:** `"averia"`
- **brigada:** `{"lider": {"CI": "123", "nombre": "Juan"}, "integrantes": [{"CI": "456", "nombre": "Pedro"}]}`
- **materiales:** `[]`
- **cliente:** `{"nombre": "Empresa X", "numero": "789"}`
- **fecha_hora:** `{"fecha": "2024-06-01", "hora": "10:00"}`
- **descripcion:** `"Se rompió la tubería principal"`
- **fotos_inicio:** (opcional)
- **fotos_fin:** (opcional)

#### Respuesta exitosa
```json
{
  "success": true,
  "message": "Reporte de avería recibido y guardado con id 12345",
  "data": { ... }
}
```

#### Nota lógica
- **El cliente debe existir previamente.** Si no existe, primero crear el cliente usando el endpoint de clientes.

---

## 4. Crear Reporte de Mantenimiento

### Endpoint
- **POST** `/api/reportes/mantenimiento`
- **Tipo de contenido:** `multipart/form-data`

### Descripción
Crea un nuevo reporte de mantenimiento. El cliente **debe existir previamente**; se asocia por su información.

### Campos requeridos
| Campo         | Tipo         | Descripción                                                                 |
|---------------|--------------|-----------------------------------------------------------------------------|
| tipo_reporte  | string       | Debe ser `"mantenimiento"`                                                  |
| brigada       | string (JSON)| Información de la brigada                                                   |
| materiales    | string (JSON)| Lista de materiales utilizados (opcional, puede ser `"[]"`)                 |
| cliente       | string (JSON)| Información del cliente                                                     |
| fecha_hora    | string (JSON)| Información de fecha y hora del trabajo                                     |
| descripcion   | string       | Descripción detallada del mantenimiento realizado                           |
| fotos_inicio  | archivo[]    | Fotos del inicio del trabajo (opcional)                                     |
| fotos_fin     | archivo[]    | Fotos del final del trabajo (opcional)                                      |

#### Ejemplo de request
- **tipo_reporte:** `"mantenimiento"`
- **brigada:** `{"lider": {"CI": "123", "nombre": "Juan"}, "integrantes": [{"CI": "456", "nombre": "Pedro"}]}`
- **materiales:** `[]`
- **cliente:** `{"nombre": "Empresa X", "numero": "789"}`
- **fecha_hora:** `{"fecha": "2024-06-01", "hora": "10:00"}`
- **descripcion:** `"Se realizó limpieza de filtros"`
- **fotos_inicio:** (opcional)
- **fotos_fin:** (opcional)

#### Respuesta exitosa
```json
{
  "success": true,
  "message": "Reporte de mantenimiento recibido y guardado con id 12345",
  "data": { ... }
}
```

#### Nota lógica
- **El cliente debe existir previamente.** Si no existe, primero crear el cliente usando el endpoint de clientes.

---

## Notas Generales para el Frontend
- Todos los campos tipo JSON deben enviarse como string (ejemplo: `{"nombre": "Empresa X"}`).
- Los archivos deben enviarse como parte de un formulario (`multipart/form-data`).
- Si un campo es opcional y no se envía, usar el valor por defecto (`[]` para listas, string vacío para textos).
- Las respuestas siempre incluyen un campo `success` y un mensaje descriptivo.
- **Resumen de lógica:**
  - Para reportes de inversión, el cliente puede ser creado en el mismo request.
  - Para reportes de avería y mantenimiento, el cliente debe existir previamente.

---

¿Dudas? Consultar con el equipo backend para detalles adicionales. 