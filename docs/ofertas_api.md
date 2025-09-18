## API de Ofertas

Base URL: `/api/ofertas`

Autenticación: Bearer Token por header `Authorization: Bearer <TOKEN>`.
- El token debe coincidir con la variable de entorno `AUTH_TOKEN` configurada en el servidor.

### Modelos

Oferta (completa)
- `id`: string (solo respuesta)
- `descripcion`: string
- `precio`: number
- `precio_cliente`?: number | null (opcional)
- `imagen`?: string | null (URL)
- `garantias`: string[]
- `elementos`: Array<{ `categoria`?: string, `foto`?: string, `descripcion`?: string, `cantidad`?: number }>

OfertaSimplificada
- `id`: string (solo respuesta)
- `descripcion`: string
- `precio`: number
- `precio_cliente`?: number | null (opcional)
- `imagen`?: string | null (URL)

### Endpoints

- GET `/simplified` — Listar ofertas simplificadas
  - Respuesta 200:
  ```json
  {
    "success": true,
    "message": "Ofertas simplificadas obtenidas",
    "data": [
      { "id": "64f7b2...", "descripcion": "Instalación de paneles", "precio": 15000.0, "precio_cliente": 14500.0, "imagen": "https://.../imagen.jpg" }
    ]
  }
  ```

- GET `/` — Listar ofertas completas
  - Respuesta 200:
  ```json
  {
    "success": true,
    "message": "Ofertas obtenidas",
    "data": [
      {
        "id": "68cac8637c536b55d0a7f12f",
        "descripcion": "Instalación de paneles solares residencial",
        "precio": 15000.0,
        "precio_cliente": 14500.0,
        "imagen": "https://example.com/imagen-oferta-1.jpg",
        "garantias": ["5 años en paneles", "2 años en instalación"],
        "elementos": [
          {"categoria": "Panel Solar", "foto": "https://example.com/panel.jpg", "descripcion": "Panel 400W", "cantidad": 10}
        ]
      }
    ]
  }
  ```

- GET `/{oferta_id}` — Obtener oferta por id
  - Respuesta 200 (encontrada):
  ```json
  {"success": true, "message": "Oferta encontrada", "data": { /* Oferta */ }}
  ```
  - Respuesta 200 (no encontrada):
  ```json
  {"success": false, "message": "Oferta no encontrada", "data": null}
  ```

- POST `/` — Crear oferta
  - Content-Type: `multipart/form-data`
  - Form data:
    - `descripcion`: string (requerido)
    - `precio`: number (requerido)
    - `precio_cliente`: number (opcional)
    - `imagen`: file (opcional - archivo de imagen)
    - `garantias`: string (JSON array, por defecto "[]")
    - `elementos`: string (JSON array, por defecto "[]")
  - Ejemplo usando curl:
  ```bash
  curl -X POST "http://localhost:8000/api/ofertas/" \
    -H "Authorization: Bearer <TOKEN>" \
    -F "descripcion=Instalación de paneles" \
    -F "precio=15000.0" \
    -F "precio_cliente=14500.0" \
    -F "imagen=@/path/to/image.jpg" \
    -F "garantias=[\"5 años en paneles\", \"2 años en instalación\"]" \
    -F "elementos=[{\"categoria\": \"Panel Solar\", \"descripcion\": \"Panel 400W\", \"cantidad\": 10}]"
  ```
  - Respuesta 200:
  ```json
  {"success": true, "message": "Oferta creada", "oferta_id": "..."}
  ```

- PUT `/{oferta_id}` — Actualizar oferta (parcial o total)
  - Content-Type: `multipart/form-data`
  - Form data (todos opcionales):
    - `descripcion`: string
    - `precio`: number
    - `precio_cliente`: number
    - `imagen`: file (archivo de imagen)
    - `garantias`: string (JSON array)
    - `elementos`: string (JSON array)
  - Ejemplo usando curl:
  ```bash
  curl -X PUT "http://localhost:8000/api/ofertas/68cac8637c536b55d0a7f12f" \
    -H "Authorization: Bearer <TOKEN>" \
    -F "descripcion=Nueva descripción" \
    -F "precio_cliente=13500.0" \
    -F "imagen=@/path/to/new-image.jpg"
  ```
  - Respuesta 200:
  ```json
  {"success": true, "message": "Oferta actualizada"}
  ```
  - Si no hay cambios o no existe:
  ```json
  {"success": false, "message": "Oferta no encontrada o sin cambios"}
  ```

- DELETE `/{oferta_id}` — Eliminar oferta
  - Respuesta 200:
  ```json
  {"success": true, "message": "Oferta eliminada"}
  ```
  - Si no existe:
  ```json
  {"success": false, "message": "Oferta no encontrada o no eliminada"}
  ```

### Cabeceras

Enviar en todas las llamadas:
```
Authorization: Bearer <TOKEN>
Accept: application/json
Content-Type: multipart/form-data (en POST/PUT con archivos)
```

### Notas
- `precio` y `precio_cliente` son number (float).
- Los campos `imagen` y `foto` son opcionales y pueden ser `null`.
- El `id` se devuelve como string.
- Las imágenes se almacenan en MinIO bucket "ofertas" y se devuelve la URL pública.
- Los campos `garantias` y `elementos` se envían como strings JSON en form-data.
- `precio_cliente` es opcional y puede usarse para precios específicos por cliente.
