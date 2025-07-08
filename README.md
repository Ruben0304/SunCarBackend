## 🧱 Estructura del Proyecto (Clean Architecture + FastAPI)

Este proyecto está organizado usando **Clean Architecture**, lo que significa que dividimos el código en capas claras para separar responsabilidades y facilitar el mantenimiento y la escalabilidad.

Aquí tenés una vista rápida de cómo está organizado todo:


# 📁 Project Structure

```
project/
├── 🧠 domain/                    # Reglas de negocio puras
│   └── 📦 entities/              # Modelos del dominio (ej: Producto, Trabajador)
├── 📋 application/               # Lógica de aplicación / Casos de uso
│   └── 🔧 services/              # Servicios que coordinan entidades y lógica
├── 🏗️ infrastructure/           # Parte técnica (DB, adaptadores)
│   ├── 📁 repositories/          # Implementaciones reales para acceder a datos
│   ├── 🛢️ database/
│   │   └── 🍃 mongodb/          # Configuración y conexión a MongoDB
│   └── 🧩 dependencies.py       # Inyección de dependencias (repos, servicios, etc.)
├── 🌐 presentation/              # Capa HTTP (lo que ve el mundo exterior)
│   └── 🚏 routers/
│       ├── 👤 admin.py          # Endpoints para admins
│       ├── 🧑‍🤝‍🧑 client.py        # Endpoints para clientes
│       └── 🔁 shared.py         # Endpoints compartidos por ambos
├── 🧪 test/                     # Tests automatizados
└── 🚀 main.py                   # Punto de entrada principal de la aplicación
```

## 📖 Descripción de las capas

### 🧠 Domain
Contiene las reglas de negocio puras y los modelos del dominio. Esta capa no depende de ninguna otra.

### 📋 Application  
Implementa los casos de uso y la lógica de aplicación que coordina las entidades del dominio.

### 🏗️ Infrastructure
Maneja todos los aspectos técnicos como bases de datos, repositorios y configuraciones externas.

### 🌐 Presentation
Expone la API REST con endpoints organizados por tipo de usuario y funcionalidades compartidas.

### 🧪 Test
Contiene todas las pruebas automatizadas del proyecto.

### 🌀 ¿Cómo se conecta todo esto?

1. **Un `router`** (por ejemplo, `admin.py`) recibe una petición HTTP.
2. Llama a un **servicio** de `application/services`, que tiene la lógica para atender esa petición.
3. El servicio usa una o varias **entidades** del `domain`.
4. Para obtener datos, el servicio le pide ayuda a un **repositorio**, que está en `infrastructure/repositories`.
5. El repositorio usa la conexión a la base de datos definida en `infrastructure/database/mongodb`.

Todo se configura y se inyecta a FastAPI en `infrastructure/dependencies.py`.

---

¿Querés probar agregar un endpoint nuevo? Fijate qué tipo de usuario lo usará (admin/client/shared), y agregalo en el router correspondiente. Después creá el servicio en `application/services`, y si necesitás datos de la DB, hacelo pasar por el repositorio.

---

Cualquier cosa, preguntame. ¡Vamos paso a paso! 🚀

## Endpoints GET añadidos para reportes y clientes

### Listar reportes (colección principal)
`GET /api/reportes`

**Parámetros opcionales:**
- `tipo_reporte`: Filtra por tipo (inversion, averia, mantenimiento)
- `cliente_numero`: Filtra por número de cliente
- `fecha_inicio`, `fecha_fin`: Filtra por rango de fechas (YYYY-MM-DD)
- `lider_ci`: Filtra por CI del líder de brigada

**Ejemplo:**
```
GET /api/reportes?tipo_reporte=inversion&cliente_numero=1400
```

### Listar reportes (vista reportes_view)
`GET /api/reportes/view`

Mismos parámetros que el anterior, pero consulta la vista agregada en MongoDB.

**Ejemplo:**
```
GET /api/reportes/view?fecha_inicio=2025-07-01&fecha_fin=2025-07-31
```

### Listar clientes
`GET /api/clientes`

**Parámetros opcionales:**
- `numero`: Filtra por número exacto
- `nombre`: Búsqueda parcial por nombre (case-insensitive)
- `direccion`: Búsqueda parcial por dirección

**Ejemplo:**
```
GET /api/clientes?nombre=Juanca
```

### Listar todos los reportes de un cliente
`GET /api/reportes/cliente/{numero}`

**Parámetros opcionales:**
- `desde_vista`: Si es true, consulta la vista agregada `reportes_view` (por defecto consulta la colección principal)
- `tipo_reporte`: Filtra por tipo de reporte (inversion, averia, mantenimiento)
- `fecha_inicio`, `fecha_fin`: Filtra por rango de fechas (YYYY-MM-DD)
- `lider_ci`: Filtra por CI del líder de brigada

**Ejemplo:**
```
GET /api/reportes/cliente/1400?tipo_reporte=inversion&fecha_inicio=2025-07-01&fecha_fin=2025-07-31
```

Todos los endpoints devuelven la estructura completa de cada entidad, incluyendo los campos particulares según el tipo de reporte.


### Obtener horas trabajadas de un trabajador
`GET /api/trabajadores/horas-trabajadas/{ci}`

**Parámetros requeridos:**
- `ci`: Cédula de identidad del trabajador (en la URL)
- `fecha_inicio`: Fecha de inicio del rango (query param, formato `YYYY-MM-DD`)
- `fecha_fin`: Fecha de fin del rango (query param, formato `YYYY-MM-DD`)

**Descripción:**
Devuelve el total de horas trabajadas por el trabajador especificado en el rango de fechas, incluyendo el detalle de actividades.

**Ejemplo:**
```
GET /api/trabajadores/horas-trabajadas/12345678?fecha_inicio=2024-01-01&fecha_fin=2024-01-31
```

**Respuesta exitosa:**
```json
{
  "success": true,
  "message": "Horas trabajadas obtenidas correctamente para CI 12345678",
  "data": {
    "ci": "12345678",
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
```

---

### Obtener horas trabajadas de todos los trabajadores
`GET /api/trabajadores/horas-trabajadas-todos`

**Parámetros requeridos:**
- `fecha_inicio`: Fecha de inicio del rango (query param, formato `YYYY-MM-DD`)
- `fecha_fin`: Fecha de fin del rango (query param, formato `YYYY-MM-DD`)

**Descripción:**
Devuelve una lista con el total de horas trabajadas de todos los trabajadores en el rango de fechas, ordenados de mayor a menor.

**Ejemplo:**
```
GET /api/trabajadores/horas-trabajadas-todos?fecha_inicio=2024-01-01&fecha_fin=2024-01-31
```

**Respuesta exitosa:**
```json
{
  "success": true,
  "message": "Horas trabajadas de todos los trabajadores obtenidas correctamente",
  "data": {
    "fecha_inicio": "2024-01-01",
    "fecha_fin": "2024-01-31",
    "total_trabajadores": 3,
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
```

