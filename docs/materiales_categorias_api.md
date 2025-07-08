# Documentación de Gestión de Materiales y Categorías

## Conceptos clave

- **Categoría**: Es un grupo de materiales, representado como un producto en la base de datos.
- **Material**: Es un insumo o recurso, con atributos como código, descripción y unidad de medida, que pertenece a una categoría.

---

## Lógica de negocio

### 1. **Gestión de Categorías**
- Una categoría se crea como un producto con un nombre y una lista opcional de materiales.
- Se pueden obtener todas las categorías únicas.
- Se pueden obtener todos los materiales de una categoría específica.

### 2. **Gestión de Materiales**
- Los materiales se almacenan dentro de la lista de materiales de cada categoría.
- Se pueden agregar materiales a una categoría existente.
- Se pueden obtener todos los materiales de una categoría.

---

## Endpoints Relacionados

### 1. Obtener todas las categorías
**GET** `/api/productos/categorias`

- **Descripción**: Devuelve la lista de todas las categorías únicas de productos/materiales.
- **Respuesta exitosa:**
  ```json
  {
    "success": true,
    "message": "Categorías obtenidas exitosamente",
    "data": [
      {"nombre": "Lubricantes"},
      {"nombre": "Repuestos"}
    ]
  }
  ```

---

### 2. Crear una nueva categoría (producto)
**POST** `/api/productos/`

- **Descripción**: Crea una nueva categoría (producto) con una lista opcional de materiales.
- **Body:**
  ```json
  {
    "categoria": "Lubricantes",
    "materiales": [
      {
        "codigo": "ACE001",
        "descripcion": "Aceite sintético",
        "um": "litro"
      }
    ]
  }
  ```
- **Respuesta exitosa:**
  ```json
  {
    "success": true,
    "message": "Producto creado exitosamente",
    "producto_id": "..."
  }
  ```

---

### 3. Obtener materiales de una categoría
**GET** `/api/productos/categorias/{categoria}/materiales`

- **Descripción**: Devuelve todos los materiales de una categoría específica.
- **Parámetro de path:**  
  - `categoria`: ID de la categoría (producto)
- **Respuesta exitosa:**
  ```json
  {
    "success": true,
    "message": "Materiales de categoría 'Lubricantes' obtenidos exitosamente",
    "data": [
      {
        "codigo": "ACE001",
        "descripcion": "Aceite sintético",
        "um": "litro"
      }
    ]
  }
  ```

---

### 4. Agregar material a una categoría existente
**POST** `/api/productos/{producto_id}/materiales`

- **Descripción**: Agrega un material a una categoría (producto) existente.
- **Parámetro de path:**  
  - `producto_id`: ID de la categoría (producto)
- **Body:**
  ```json
  {
    "material": {
      "codigo": "ACE002",
      "descripcion": "Aceite mineral",
      "um": "litro"
    }
  }
  ```
- **Respuesta exitosa:**
  ```json
  {
    "success": true,
    "message": "Material agregado exitosamente"
  }
  ```

---

### 5. Obtener todos los productos (categorías con materiales)
**GET** `/api/productos/`

- **Descripción**: Devuelve todas las categorías con sus materiales.
- **Respuesta exitosa:**
  ```json
  {
    "success": true,
    "message": "Productos obtenidos exitosamente",
    "data": [
      {
        "id": "123",
        "categoria": "Lubricantes",
        "materiales": [
          {
            "codigo": "ACE001",
            "descripcion": "Aceite sintético",
            "um": "litro"
          }
        ]
      }
    ]
  }
  ```

---

## Validaciones y reglas

- **Al crear o agregar materiales:**
  - El código, descripción y unidad de medida no pueden estar vacíos.
  - La cantidad, si aplica, debe ser un número mayor a 0.
- **Al crear una categoría:**
  - El nombre de la categoría no puede estar vacío.
  - Los materiales son opcionales al crear la categoría.
- **Al agregar un material:**
  - Se agrega a la lista de materiales de la categoría (producto) correspondiente.

---

## Ejemplo de uso

### Crear una categoría con materiales
```bash
curl -X POST "http://localhost:8000/api/productos/" \
  -H "Content-Type: application/json" \
  -d '{
    "categoria": "Lubricantes",
    "materiales": [
      {
        "codigo": "ACE001",
        "descripcion": "Aceite sintético",
        "um": "litro"
      }
    ]
  }'
```

### Agregar un material a una categoría existente
```bash
curl -X POST "http://localhost:8000/api/productos/123456/materiales" \
  -H "Content-Type: application/json" \
  -d '{
    "material": {
      "codigo": "ACE002",
      "descripcion": "Aceite mineral",
      "um": "litro"
    }
  }'
```

---

## Resumen

- **Las categorías** agrupan materiales y se gestionan como productos.
- **Los materiales** se agregan, consultan y validan siempre dentro de una categoría.
- **Los endpoints permiten** crear, consultar y modificar tanto categorías como materiales de forma flexible y validada. 