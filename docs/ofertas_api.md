## API de Ofertas

Base URL: `/api/ofertas`

Autenticación: Header `Authorization: suncar-token-2025` (igual que el resto de endpoints protegidos del backend).

### Modelo

Oferta
- `id`: string (solo respuesta)
- `descripcion`: string
- `precio`: number
- `garantias`: string[]
- `elementos`: Array<{ `categoria`?: string, `foto`?: string, `descripcion`?: string, `cantidad`?: number }>

### Endpoints

- GET `/` — Listar ofertas
  - Respuesta 200:
  ```json
  {
    "success": true,
    "message": "Ofertas obtenidas",
    "data": [
      {
        "id": "68cac8637c536b55d0a7f12f",
        "descripcion": "Oferta de electrónica básica",
        "precio": 299.99,
        "garantias": ["Garantía de fábrica 1 año", "Repuestos garantizados"],
        "elementos": [
          {"categoria": "electrónica", "foto": "https://ejemplo.com/telefono.jpg", "descripcion": "Teléfono inteligente", "cantidad": 1},
          {"categoria": "accesorios", "foto": "https://ejemplo.com/funda.jpg", "descripcion": "Funda protectora", "cantidad": 2}
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
  - Body:
  ```json
  {
    "descripcion": "string",
    "precio": 0,
    "garantias": ["string"],
    "elementos": [
      {"categoria": "string", "foto": "url", "descripcion": "string", "cantidad": 1}
    ]
  }
  ```
  - Respuesta 200:
  ```json
  {"success": true, "message": "Oferta creada", "oferta_id": "..."}
  ```

- PUT `/{oferta_id}` — Actualizar oferta (parcial o total)
  - Body: objeto parcial con cualquier campo de `Oferta` excepto `id`.
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
Authorization: suncar-token-2025
Accept: application/json
Content-Type: application/json (en POST/PUT)
```

### Notas
- Campos opcionales en `elementos`: `categoria`, `foto`, `descripcion`, `cantidad` pueden omitirse según el caso de uso.
- `precio` es number (float).
- El `id` se devuelve como string.


