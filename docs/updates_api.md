# API de Actualizaciones - SunCar Backend

Esta API permite a la aplicación móvil verificar si tiene datos desactualizados o si la aplicación misma necesita ser actualizada.

## Endpoints

### 1. Verificar Actualización de Datos

**POST** `/api/update/data`

Verifica si los datos de la aplicación están actualizados comparando timestamps.

#### Request Body

```json
{
  "last_update_timestamp": "2024-01-15T10:30:00Z"
}
```

#### Response

```json
{
  "is_up_to_date": false,
  "outdated_entities": ["materiales", "trabajadores"],
  "current_timestamp": "2024-01-16T14:20:00Z"
}
```

#### Campos de Respuesta

- `is_up_to_date`: Boolean que indica si todos los datos están actualizados
- `outdated_entities`: Lista de entidades que necesitan actualización
- `current_timestamp`: Timestamp actual del servidor

### 2. Verificar Actualización de Aplicación

**POST** `/api/update/application`

Verifica si la aplicación móvil está actualizada.

#### Request Body

```json
{
  "current_version": "1.1.0",
  "platform": "android"
}
```

#### Response (App Desactualizada)

```json
{
  "is_up_to_date": false,
  "latest_version": "1.2.0",
  "download_url": "https://example.com/app-v1.2.0.apk",
  "file_size": 15728640,
  "changelog": "Nuevas funcionalidades y correcciones de bugs",
  "force_update": false
}
```

#### Response (App Actualizada)

```json
{
  "is_up_to_date": true
}
```

#### Campos de Respuesta

- `is_up_to_date`: Boolean que indica si la app está actualizada
- `latest_version`: Versión más reciente disponible (solo si no está actualizada)
- `download_url`: URL directa para descargar la actualización
- `file_size`: Tamaño del archivo en bytes
- `changelog`: Descripción de los cambios
- `force_update`: Boolean que indica si la actualización es obligatoria

### 3. Estado del Sistema

**GET** `/api/update/status`

Obtiene información general sobre el estado de las actualizaciones.

#### Response

```json
{
  "system_status": "operational",
  "last_check": "2024-01-16T14:20:00",
  "available_entities": ["materiales", "trabajadores", "clientes"],
  "app_versions": {
    "android": "1.2.0",
    "ios": "1.2.0"
  }
}
```

## Entidades Soportadas

- **materiales**: Catálogo de productos y materiales
- **trabajadores**: Lista de trabajadores
- **clientes**: Información de clientes

## Plataformas Soportadas

- **android**: Aplicación Android
- **ios**: Aplicación iOS

## Optimizaciones Implementadas

1. **Compresión**: Los endpoints soportan compresión gzip automática
2. **Cache**: Se pueden agregar headers de cache para optimizar las consultas
3. **Validación de Versiones**: Comparación semántica de versiones (1.2.0 > 1.1.0)
4. **Manejo de Errores**: Respuestas de error detalladas y consistentes

## Ejemplo de Uso en la App Móvil

```javascript
// Verificar datos
const checkDataUpdates = async () => {
  const response = await fetch("/api/update/data", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      last_update_timestamp: lastKnownUpdate,
    }),
  });

  const result = await response.json();

  if (!result.is_up_to_date) {
    // Actualizar entidades específicas
    for (const entity of result.outdated_entities) {
      await updateEntity(entity);
    }
  }
};

// Verificar app
const checkAppUpdates = async () => {
  const response = await fetch("/api/update/application", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      current_version: appVersion,
      platform: "android",
    }),
  });

  const result = await response.json();

  if (!result.is_up_to_date) {
    if (result.force_update) {
      // Mostrar diálogo obligatorio
      showForceUpdateDialog(result.download_url);
    } else {
      // Mostrar diálogo opcional
      showOptionalUpdateDialog(result);
    }
  }
};
```

## Configuración

Las versiones de la aplicación se configuran en el `UpdateService`. En producción, se recomienda:

1. Mover la configuración a una base de datos
2. Implementar un panel de administración para gestionar versiones
3. Agregar logs para monitorear las actualizaciones
4. Implementar rate limiting para evitar abuso
