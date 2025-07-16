# API de Trabajadores y Brigadas

## Endpoints de Trabajadores

### 1. Eliminar Trabajador
**DELETE** `/trabajadores/{ci}`

Elimina un trabajador de la base de datos por su cédula de identidad.

**Parámetros:**
- `ci` (path): Cédula de identidad del trabajador a eliminar

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "message": "Trabajador con CI 12345678 eliminado exitosamente."
}
```

**Respuesta de error (404):**
```json
{
  "detail": "Trabajador con CI 12345678 no encontrado."
}
```

---

### 2. Actualizar Datos del Trabajador
**PUT** `/trabajadores/{ci}`

Actualiza el nombre y opcionalmente el CI de un trabajador.

**Parámetros:**
- `ci` (path): Cédula de identidad actual del trabajador

**Body:**
```json
{
  "nombre": "Nuevo Nombre",
  "nuevo_ci": "87654321"  // Opcional
}
```

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "message": "Trabajador con CI 12345678 actualizado exitosamente."
}
```

**Respuesta de error (404):**
```json
{
  "detail": "Trabajador con CI 12345678 no encontrado."
}
```

---

### 3. Eliminar Trabajador de Brigada
**DELETE** `/trabajadores/{ci}/brigada/{brigada_id}`

Elimina un trabajador de una brigada específica sin eliminarlo de la base de datos.

**Parámetros:**
- `ci` (path): Cédula de identidad del trabajador
- `brigada_id` (path): ID de la brigada

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "message": "Trabajador con CI 12345678 eliminado de la brigada exitosamente."
}
```

**Respuesta de error (404):**
```json
{
  "detail": "Trabajador o brigada no encontrados."
}
```

---

## Endpoints de Brigadas

### 1. Eliminar Brigada
**DELETE** `/brigadas/{brigada_id}`

Elimina completamente una brigada de la base de datos.

**Parámetros:**
- `brigada_id` (path): ID de la brigada a eliminar

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "message": "Brigada eliminada exitosamente"
}
```

**Respuesta de error (404):**
```json
{
  "success": false,
  "message": "Brigada no encontrada"
}
```

---

### 2. Eliminar Trabajador de Brigada (Alternativo)
**DELETE** `/brigadas/{brigada_id}/trabajadores/{trabajador_ci}`

Elimina un trabajador específico de una brigada (endpoint alternativo).

**Parámetros:**
- `brigada_id` (path): ID de la brigada
- `trabajador_ci` (path): Cédula de identidad del trabajador

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "message": "Trabajador eliminado de la brigada exitosamente"
}
```

**Respuesta de error (404):**
```json
{
  "success": false,
  "message": "Brigada o trabajador no encontrado"
}
```

---

## Códigos de Estado HTTP

- **200**: Operación exitosa
- **201**: Recurso creado exitosamente
- **404**: Recurso no encontrado
- **500**: Error interno del servidor

## Notas Importantes

1. **Eliminación de Trabajador**: Al eliminar un trabajador, se elimina completamente de la base de datos. Si solo quieres removerlo de una brigada, usa el endpoint de "Eliminar Trabajador de Brigada".

2. **Actualización de CI**: Al actualizar el CI de un trabajador, el nuevo CI debe ser único en la base de datos.

3. **Eliminación de Brigada**: Al eliminar una brigada, se eliminan todas las relaciones con trabajadores, pero los trabajadores permanecen en la base de datos.

4. **IDs de Brigada**: Los IDs de brigada pueden ser ObjectIds de MongoDB o CIs de líderes, dependiendo del contexto.

## Ejemplos de Uso

### Eliminar un trabajador
```javascript
fetch('/trabajadores/12345678', {
  method: 'DELETE'
})
.then(response => response.json())
.then(data => console.log(data));
```

### Actualizar datos de trabajador
```javascript
fetch('/trabajadores/12345678', {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    nombre: 'Juan Pérez',
    nuevo_ci: '87654321'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

### Eliminar trabajador de brigada
```javascript
fetch('/trabajadores/12345678/brigada/brigada123', {
  method: 'DELETE'
})
.then(response => response.json())
.then(data => console.log(data));
```

### Eliminar brigada
```javascript
fetch('/brigadas/brigada123', {
  method: 'DELETE'
})
.then(response => response.json())
.then(data => console.log(data));
``` 