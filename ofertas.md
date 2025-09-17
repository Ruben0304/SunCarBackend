# API de Ofertas - Documentación para Frontend

## Endpoints Base
Todos los endpoints están bajo: `/api/ofertas`

## Autenticación
Todos los endpoints requieren el header de autorización:
```
Authorization: suncar-token-2025
```

## Modelos de Datos

### OfertaSimplificada
```typescript
interface OfertaSimplificada {
  id?: string | null;
  descripcion: string;
  precio: number;
  imagen?: string | null;      // URL de imagen
}
```

### Oferta (Completa)
```typescript
interface Oferta {
  id?: string | null;
  descripcion: string;
  precio: number;
  imagen?: string | null;      // URL de imagen
  garantias: string[];
  elementos: OfertaElemento[];
}

interface OfertaElemento {
  categoria?: string | null;
  foto?: string | null;        // URL de imagen
  descripcion?: string | null;
  cantidad?: number | null;
}
```

## Endpoints

### 1. Obtener ofertas simplificadas

**GET** `/api/ofertas/simplified`

**Caso de uso**: Página de listado de ofertas. Solo devuelve información básica para mostrar en cards o listas.

#### Response
```typescript
{
  success: boolean;
  message: string;
  data: OfertaSimplificada[];
}
```

#### Ejemplo
```json
{
  "success": true,
  "message": "Ofertas simplificadas obtenidas",
  "data": [
    {
      "id": "64f7b2a3c1234567890abcde",
      "descripcion": "Instalación de paneles solares residencial",
      "precio": 15000.0,
      "imagen": "https://example.com/imagen-oferta-1.jpg"
    }
  ]
}
```

---

### 2. Obtener todas las ofertas completas

**GET** `/api/ofertas/`

**Caso de uso**: Vista administrativa. Devuelve todas las ofertas con información completa incluyendo garantías y elementos.

#### Response
```typescript
{
  success: boolean;
  message: string;
  data: Oferta[];
}
```

#### Ejemplo
```json
{
  "success": true,
  "message": "Ofertas obtenidas",
  "data": [
    {
      "id": "64f7b2a3c1234567890abcde",
      "descripcion": "Instalación de paneles solares residencial",
      "precio": 15000.0,
      "imagen": "https://example.com/imagen-oferta-1.jpg",
      "garantias": ["5 años en paneles", "2 años en instalación"],
      "elementos": [
        {
          "categoria": "Panel Solar",
          "foto": "https://example.com/panel-solar.jpg",
          "descripcion": "Panel solar monocristalino 400W",
          "cantidad": 10
        }
      ]
    }
  ]
}
```

---

### 3. Obtener oferta por ID

**GET** `/api/ofertas/{oferta_id}`

**Caso de uso**: Vista detallada de una oferta específica. Devuelve información completa de una sola oferta.

#### Response
```typescript
{
  success: boolean;
  message: string;
  data: Oferta | null;
}
```

#### Ejemplo (encontrada)
```json
{
  "success": true,
  "message": "Oferta encontrada",
  "data": {
    "id": "64f7b2a3c1234567890abcde",
    "descripcion": "Instalación de paneles solares residencial",
    "precio": 15000.0,
    "imagen": "https://example.com/imagen-oferta-1.jpg",
    "garantias": ["5 años en paneles", "2 años en instalación"],
    "elementos": [...]
  }
}
```

#### Ejemplo (no encontrada)
```json
{
  "success": false,
  "message": "Oferta no encontrada",
  "data": null
}
```

## Códigos de Estado
- **200**: Éxito (incluso si no se encuentra contenido)
- **500**: Error interno del servidor

## Notas Importantes
- Todas las imágenes son URLs, no base64
- Los campos `imagen` y `foto` son opcionales y pueden ser `null`
- Siempre verificar el campo `success` antes de usar `data`