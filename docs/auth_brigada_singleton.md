# Sistema de Autenticación con Brigada Singleton

## Descripción

Se ha implementado un sistema de autenticación mejorado que:

1. **Autentica trabajadores** usando CI y contraseña
2. **Retorna la brigada** de la cual el trabajador es líder (si existe)
3. **Almacena la brigada** en un singleton para uso global en la aplicación

## Componentes Principales

### 1. AuthService Modificado

El `AuthService` ahora:
- Recibe tanto `WorkerRepository` como `BrigadaRepository`
- Retorna `Optional[Brigada]` en lugar de `bool`
- Busca automáticamente la brigada del líder después de una autenticación exitosa

### 2. BrigadaSingleton

Clase singleton que mantiene la brigada activa:
- `set_brigada_activa(brigada)`: Establece la brigada activa
- `get_brigada_activa()`: Obtiene la brigada activa
- `clear_brigada_activa()`: Limpia la brigada activa (logout)
- `has_brigada_activa()`: Verifica si hay una brigada activa

### 3. Endpoints Actualizados

#### POST `/api/auth/trabajador`
```json
{
  "ci": "12345678",
  "contraseña": "password123"
}
```

**Respuesta exitosa:**
```json
{
  "success": true,
  "message": "Autenticación exitosa",
  "brigada": {
    "lider_ci": "12345678",
    "lider": {
      "id": "...",
      "CI": "12345678",
      "nombre": "Juan Pérez",
      // ... otros campos del trabajador
    },
    "integrantes": [
      // ... lista de integrantes de la brigada
    ]
  }
}
```

**Respuesta fallida:**
```json
{
  "success": false,
  "message": "Credenciales incorrectas o trabajador no es líder de brigada",
  "brigada": null
}
```

#### GET `/api/auth/brigada-activa`
Retorna la brigada actualmente activa en el singleton.

#### POST `/api/auth/logout`
Limpia la brigada activa del singleton.

## Flujo de Uso

1. **Login**: El trabajador se autentica con CI y contraseña
2. **Verificación**: Se verifica si las credenciales son correctas
3. **Búsqueda de Brigada**: Si la autenticación es exitosa, se busca la brigada donde es líder
4. **Almacenamiento**: La brigada se almacena en el singleton
5. **Respuesta**: Se retorna la brigada completa con líder e integrantes

## Casos de Uso

### Caso 1: Trabajador es líder de brigada
- Login exitoso
- Brigada encontrada y almacenada en singleton
- Respuesta incluye datos completos de la brigada

### Caso 2: Trabajador no es líder de brigada
- Login exitoso (credenciales correctas)
- No se encuentra brigada donde sea líder
- Respuesta indica que no es líder de brigada

### Caso 3: Credenciales incorrectas
- Login fallido
- No se busca brigada
- Respuesta indica credenciales incorrectas

## Ventajas del Sistema

1. **Eficiencia**: La brigada se busca solo una vez durante el login
2. **Acceso Global**: Cualquier parte de la aplicación puede acceder a la brigada activa
3. **Persistencia**: La brigada permanece disponible durante toda la sesión
4. **Flexibilidad**: Permite trabajadores que no son líderes de brigada

## Uso en Otros Servicios

Para usar la brigada activa en otros servicios:

```python
from application.singleton.brigada_singleton import BrigadaSingleton

# Obtener la brigada activa
brigada_activa = BrigadaSingleton.get_brigada_activa()

if brigada_activa:
    # Usar la brigada activa
    lider = brigada_activa.lider
    integrantes = brigada_activa.integrantes
else:
    # No hay brigada activa
    pass
``` 