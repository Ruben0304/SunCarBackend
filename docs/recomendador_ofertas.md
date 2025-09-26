# Sistema Recomendador de Ofertas

Sistema de recomendaciones inteligente que utiliza IA para ordenar todas las ofertas según la consulta del usuario.

## Endpoint

```
POST /api/ofertas/recomendador
```

## Request

### Parámetros de entrada

```json
{
  "texto": "string"
}
```

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `texto` | string | Sí | Consulta del usuario describiendo lo que busca |

### Ejemplo de request

```json
{
  "texto": "Busco algo económico para el hogar"
}
```

## Response

### Respuesta exitosa (200)

```json
{
  "success": true,
  "message": "Recomendaciones generadas exitosamente",
  "data": {
    "texto": "string",
    "ofertas": [OfertaSimplificada]
  }
}
```

#### Estructura de `data`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `texto` | string | Explicación generada por IA del ordenamiento realizado |
| `ofertas` | array | Lista de ofertas ordenadas de mayor a menor recomendación |

#### Estructura de `OfertaSimplificada`

```json
{
  "id": "string",
  "descripcion": "string",
  "precio": number,
  "precio_cliente": number | null,
  "imagen": "string" | null,
  "moneda": "string" | null,
  "financiamiento": boolean
}
```

### Respuestas de error

#### Sin ofertas disponibles (200)

```json
{
  "success": false,
  "message": "No hay ofertas disponibles para recomendar"
}
```

#### Error del servidor (500)

```json
{
  "detail": "Error al generar recomendaciones: {detalle_del_error}"
}
```

#### Request inválido (422)

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "texto"],
      "msg": "Field required"
    }
  ]
}
```

## Comportamiento del Sistema

1. **Entrada**: El usuario envía un texto describiendo lo que busca
2. **Procesamiento**: La IA analiza todas las ofertas usando el campo `descripcion_detallada` de la BD
3. **Ordenamiento**: Retorna TODAS las ofertas ordenadas de mayor a menor recomendación
4. **Formato**: Las ofertas se retornan en formato simplificado (mismo que `/simplified`)

## Relación con Ofertas Simplified

El campo `ofertas` en la respuesta contiene exactamente la misma estructura que el endpoint `/api/ofertas/simplified`, pero con dos diferencias clave:

- **Orden**: Las ofertas están ordenadas por recomendación (no orden original)
- **Filtro**: Solo incluye ofertas que tienen `descripcion_detallada` en la BD

## Ejemplos de Uso

### Consulta económica
```json
// Request
{
  "texto": "Necesito productos baratos para casa"
}

// Response
{
  "success": true,
  "message": "Recomendaciones generadas exitosamente",
  "data": {
    "texto": "Hola, aquí tienes las ofertas ordenadas de mayor a menor recomendación enfocándome en opciones económicas para el hogar...",
    "ofertas": [/* ofertas ordenadas por precio y utilidad doméstica */]
  }
}
```

### Consulta específica
```json
// Request
{
  "texto": "Equipos de computación para oficina empresarial"
}

// Response
{
  "data": {
    "texto": "He ordenado las ofertas priorizando equipos profesionales y soluciones empresariales...",
    "ofertas": [/* ofertas ordenadas por relevancia tecnológica */]
  }
}
```

## Notas Técnicas

- El sistema usa el campo `descripcion_detallada` de la BD como contexto para la IA
- Fallback automático en caso de error: ordenamiento alfabético
- Validación automática de respuesta IA usando Pydantic
- Mantiene orden de IDs retornados por la IA al obtener ofertas completas