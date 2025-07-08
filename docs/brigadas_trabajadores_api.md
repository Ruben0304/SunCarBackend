# Documentación de Endpoints - Gestión de Brigadas y Trabajadores

## Base URL
```
http://localhost:8000/api
```

---

## 1. ENDPOINTS DE BRIGADAS

### 1.1 Listar Brigadas
**GET** `/brigadas/`

**Descripción:** Obtiene todas las brigadas con sus líderes e integrantes. Permite búsqueda opcional por nombre.

**Parámetros de Query:**
- `search` (opcional): String para filtrar brigadas por nombre del líder o integrantes

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "message": "Todas las brigadas obtenidas exitosamente",
  "data": [
    {
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
    }
  ]
}
```

**Respuesta con Búsqueda:**
```json
{
  "success": true,
  "message": "Brigadas filtradas obtenidas exitosamente",
  "data": [...]
}
```

---

### 1.2 Obtener Brigada Específica
**GET** `/brigadas/{brigada_id}`

**Descripción:** Obtiene los detalles de una brigada específica por su ID.

**Parámetros de Path:**
- `brigada_id`: String - ID de la brigada (CI del líder)

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "message": "Brigada obtenida exitosamente",
  "data": {
    "lider": {
      "nombre": "Juan Pérez",
      "CI": "12345678"
    },
    "integrantes": [...]
  }
}
```

**Respuesta de Error (404):**
```json
{
  "success": false,
  "message": "Brigada no encontrada",
  "data": null
}
```

---

### 1.3 Crear Brigada
**POST** `/brigadas/`

**Descripción:** Crea una nueva brigada con un líder y lista de trabajadores.

**Código de Respuesta:** 201

**Body Request:**
```json
{
  "lider": {
    "nombre": "Juan Pérez",
    "CI": "12345678"
  },
  "integrantes": [
    {
      "nombre": "María García",
      "CI": "87654321"
    },
    {
      "nombre": "Carlos López",
      "CI": "11223344"
    }
  ]
}
```

**Validaciones:**
- El nombre no puede estar vacío
- La CI debe contener solo números y guiones
- No puede haber integrantes con la misma CI

**Respuesta Exitosa (201):**
```json
{
  "success": true,
  "message": "Brigada creada exitosamente",
  "brigada_id": "generated_id"
}
```

---

### 1.4 Editar Brigada
**PUT** `/brigadas/{brigada_id}`

**Descripción:** Actualiza una brigada existente (líder o trabajadores).

**Parámetros de Path:**
- `brigada_id`: String - ID de la brigada

**Body Request:** (Mismo formato que crear brigada)

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "message": "Brigada actualizada exitosamente"
}
```

**Respuesta de Error:**
```json
{
  "success": false,
  "message": "Brigada no encontrada o sin cambios"
}
```

---

### 1.5 Eliminar Brigada
**DELETE** `/brigadas/{brigada_id}`

**Descripción:** Elimina una brigada existente.

**Parámetros de Path:**
- `brigada_id`: String - ID de la brigada

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "message": "Brigada eliminada exitosamente"
}
```

**Respuesta de Error:**
```json
{
  "success": false,
  "message": "Brigada no encontrada"
}
```

---

### 1.6 Agregar Trabajador a Brigada
**POST** `/brigadas/{brigada_id}/trabajadores`

**Descripción:** Agrega un trabajador a una brigada existente.

**Parámetros de Path:**
- `brigada_id`: String - ID de la brigada

**Body Request:**
```json
{
  "nombre": "Nuevo Trabajador",
  "CI": "99887766"
}
```

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "message": "Trabajador agregado a la brigada exitosamente"
}
```

**Respuesta de Error:**
```json
{
  "success": false,
  "message": "Brigada no encontrada o trabajador ya es integrante"
}
```

---

### 1.7 Eliminar Trabajador de Brigada
**DELETE** `/brigadas/{brigada_id}/trabajadores/{trabajador_ci}`

**Descripción:** Elimina un trabajador de una brigada.

**Parámetros de Path:**
- `brigada_id`: String - ID de la brigada
- `trabajador_ci`: String - CI del trabajador a eliminar

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "message": "Trabajador eliminado de la brigada exitosamente"
}
```

**Respuesta de Error:**
```json
{
  "success": false,
  "message": "Brigada o trabajador no encontrado"
}
```

---

### 1.8 Editar Trabajador en Brigada
**PUT** `/brigadas/{brigada_id}/trabajadores/{trabajador_ci}`

**Descripción:** Actualiza los datos de un trabajador en una brigada.

**Parámetros de Path:**
- `brigada_id`: String - ID de la brigada
- `trabajador_ci`: String - CI del trabajador a editar

**Body Request:**
```json
{
  "nombre": "Nombre Actualizado",
  "CI": "99887766"
}
```

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "message": "Trabajador actualizado exitosamente"
}
```

---

## 2. ENDPOINTS DE TRABAJADORES

### 2.1 Listar Trabajadores
**GET** `/trabajadores/`

**Descripción:** Obtiene la lista de todos los trabajadores.

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "message": "Trabajadores obtenidos exitosamente",
  "data": [
    {
      "CI": "12345678",
      "nombre": "Juan Pérez",
      "contrasena": "hashed_password"
    }
  ]
}
```

---

### 2.2 Crear Trabajador
**POST** `/trabajadores/`

**Descripción:** Crea un nuevo trabajador con contraseña opcional.

**Body Request:**
```json
{
  "ci": "12345678",
  "nombre": "Juan Pérez",
  "contrasena": "password123"
}
```

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "message": "Trabajador creado exitosamente",
  "trabajador_id": "generated_id"
}
```

---

### 2.3 Buscar Trabajadores
**GET** `/trabajadores/buscar`

**Descripción:** Busca trabajadores por nombre (búsqueda case-insensitive).

**Parámetros de Query:**
- `nombre`: String - Nombre a buscar (requerido)

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "message": "Búsqueda completada exitosamente",
  "data": [
    {
      "CI": "12345678",
      "nombre": "Juan Pérez"
    }
  ]
}
```

---

### 2.4 Crear Jefe de Brigada
**POST** `/trabajadores/jefes_brigada`

**Descripción:** Crea un nuevo jefe de brigada con integrantes opcionales.

**Body Request:**
```json
{
  "ci": "12345678",
  "nombre": "Juan Pérez",
  "contrasena": "password123",
  "integrantes": ["87654321", "11223344"]
}
```

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "message": "Jefe de brigada creado exitosamente",
  "trabajador_id": "generated_id"
}
```

---

### 2.5 Convertir Trabajador a Jefe
**POST** `/trabajadores/{ci}/convertir_jefe`

**Descripción:** Convierte un trabajador existente en jefe de brigada.

**Parámetros de Path:**
- `ci`: String - CI del trabajador

**Body Request:**
```json
{
  "contrasena": "password123",
  "integrantes": ["87654321", "11223344"]
}
```

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "message": "Trabajador convertido a jefe de brigada exitosamente"
}
```

**Respuesta de Error:**
```json
{
  "success": false,
  "message": "Trabajador no encontrado o ya es jefe de brigada"
}
```

---

### 2.6 Crear Trabajador y Asignar Brigada
**POST** `/trabajadores/asignar_brigada`

**Descripción:** Crea un trabajador y lo asigna a una brigada existente.

**Body Request:**
```json
{
  "ci": "12345678",
  "nombre": "Juan Pérez",
  "brigada_id": "brigada_123",
  "contrasena": "password123"
}
```

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "message": "Trabajador creado y asignado a brigada exitosamente"
}
```

**Respuesta de Error:**
```json
{
  "success": false,
  "message": "Brigada no encontrada o trabajador ya existe"
}
```

---

### 2.7 Obtener Horas Trabajadas por CI
**GET** `/trabajadores/horas-trabajadas/{ci}`

**Descripción:** Obtiene el total de horas trabajadas por una persona en un rango de fechas específico.

**Parámetros de Path:**
- `ci`: String - Cédula de identidad de la persona

**Parámetros de Query:**
- `fecha_inicio`: String - Fecha de inicio del rango (formato: YYYY-MM-DD)
- `fecha_fin`: String - Fecha de fin del rango (formato: YYYY-MM-DD)

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "message": "Horas trabajadas obtenidas exitosamente",
  "data": {
    "ci": "12345678",
    "nombre": "Juan Pérez",
    "total_horas": 45.5,
    "fecha_inicio": "2024-01-01",
    "fecha_fin": "2024-01-31"
  }
}
```

---

### 2.8 Obtener Horas Trabajadas de Todos los Trabajadores
**GET** `/trabajadores/horas-trabajadas-todos`

**Descripción:** Obtiene el total de horas trabajadas de todos los trabajadores en un rango de fechas específico.

**Parámetros de Query:**
- `fecha_inicio`: String - Fecha de inicio del rango (formato: YYYY-MM-DD)
- `fecha_fin`: String - Fecha de fin del rango (formato: YYYY-MM-DD)

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "message": "Horas trabajadas de todos los trabajadores obtenidas exitosamente",
  "data": [
    {
      "ci": "12345678",
      "nombre": "Juan Pérez",
      "total_horas": 45.5
    },
    {
      "ci": "87654321",
      "nombre": "María García",
      "total_horas": 38.0
    }
  ]
}
```

---

## 3. CÓDIGOS DE ERROR COMUNES

### 3.1 Error de Validación (422)
```json
{
  "detail": [
    {
      "loc": ["body", "lider", "nombre"],
      "msg": "El nombre no puede estar vacío",
      "type": "value_error"
    }
  ]
}
```

### 3.2 Error Interno del Servidor (500)
```json
{
  "detail": "Error interno del servidor"
}
```

### 3.3 Error de Recurso No Encontrado (404)
```json
{
  "success": false,
  "message": "Recurso no encontrado"
}
```

---

## 4. NOTAS IMPORTANTES

### 4.1 Autenticación
- Algunos endpoints pueden requerir autenticación
- Las contraseñas se almacenan hasheadas en la base de datos

### 4.2 Validaciones
- Los nombres no pueden estar vacíos
- Las CIs deben contener solo números y guiones
- No se permiten CIs duplicadas en una misma brigada
- Las fechas deben estar en formato YYYY-MM-DD
- Las horas deben estar en formato HH:MM

### 4.3 Cálculo de Horas Trabajadas
- Se calculan basándose en todas las actividades donde la persona aparece como líder o integrante de brigada
- Los resultados se ordenan por total de horas trabajadas de mayor a menor
- Incluye actividades de inversión, mantenimiento y averías

### 4.4 Estructura de Brigadas
- Cada brigada tiene un líder obligatorio
- Los integrantes son opcionales
- Un trabajador puede ser líder de una brigada e integrante de otra
- Las brigadas se identifican por el CI del líder

---

## 5. EJEMPLOS DE USO

### 5.1 Crear una Brigada Completa
```bash
curl -X POST "http://localhost:8000/api/brigadas/" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

### 5.2 Buscar Trabajadores
```bash
curl -X GET "http://localhost:8000/api/trabajadores/buscar?nombre=Juan"
```

### 5.3 Obtener Horas Trabajadas
```bash
curl -X GET "http://localhost:8000/api/trabajadores/horas-trabajadas/12345678?fecha_inicio=2024-01-01&fecha_fin=2024-01-31"
``` 