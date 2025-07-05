from fastapi import APIRouter, Depends, Body, Query, HTTPException
from typing import List, Optional

from pydantic import BaseModel

from application.services.client_service import ClientService
from application.services.product_service import ProductService
from application.services.worker_service import WorkerService
from application.services.auth_service import AuthService
from domain.entities.cliente import Cliente
from domain.entities.producto import CatalogoProductos, Material, Cataegoria
from domain.entities.trabajador import Trabajador
from domain.entities.brigada import Brigada
from infrastucture.dependencies import get_product_service, get_worker_service, get_auth_service, \
    get_brigada_repository, get_client_service
from infrastucture.repositories.brigada_repository import BrigadaRepository
from presentation.schemas.requests.ClienteCreateRequest import ClienteCreateRequest, ClienteCreateSimpleRequest

router = APIRouter()


class LoginRequest(BaseModel):
    ci: str
    contraseña: str


class LoginResponse(BaseModel):
    success: bool
    message: str
    brigada: Optional[Brigada] = None


@router.get("/productos_por_tipo_y_marca", response_model=List[CatalogoProductos])
async def read_products(
        product_service: ProductService = Depends(get_product_service)
):
    """
    Endpoint para obtener una lista de todos los productos.
    """
    try:
        products = await product_service.get_all_products()
        return products
    except Exception as e:
        raise HTTPException()


@router.get("/categorias", response_model=List[Cataegoria])
async def read_categories(
        product_service: ProductService = Depends(get_product_service)
):
    """
    Endpoint para obtener una lista de todas las categorías únicas de productos.
    """
    try:
        categories = await product_service.get_unique_categories()
        return categories
    except Exception as e:
        raise HTTPException()


@router.get("/categorias/{categoria}/materiales", response_model=List[Material])
async def read_materials_by_category(
        categoria: str,
        product_service: ProductService = Depends(get_product_service)
):
    """
    Endpoint para obtener todos los materiales únicos de una categoría específica.
    """
    try:
        materials = await product_service.get_materials_by_category(categoria)
        return materials
    except Exception as e:
        raise HTTPException()


@router.get("/trabajadores", response_model=List[Trabajador])
async def read_workers(
        worker_service: WorkerService = Depends(get_worker_service)
):
    """
    Endpoint to get a list of all workers.
    """
    try:
        workers = await worker_service.get_all_workers()
        return workers
    except Exception as e:
        raise HTTPException()

@router.post("/auth/trabajador", response_model=LoginResponse)
async def login_trabajador(
        login_data: LoginRequest,
        auth_service: AuthService = Depends(get_auth_service)
):
    """
    Endpoint para autenticar un trabajador usando CI y contraseña.
    Si la autenticación es exitosa, retorna la brigada de la cual es líder.
    """
    try:
        brigada = await auth_service.login_trabajador(login_data.ci, login_data.contraseña)
        
        if brigada is not None:
            
            return LoginResponse(
                success=True,
                message="Autenticación exitosa",
                brigada=brigada
            )
        else:
            return LoginResponse(
                success=False,
                message="Credenciales incorrectas o trabajador no es líder de brigada",
                brigada=None
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/productos", response_model=str, status_code=201)
async def crear_producto(
    categoria: str = Body(..., embed=True),
    materiales: Optional[list] = Body(default=None),
    product_service: ProductService = Depends(get_product_service)
):
    """
    Crear un nuevo producto (categoría) con materiales opcionales.
    """
    try:
        producto_id = await product_service.create_product(categoria, materiales)
        return producto_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/productos/{producto_id}/materiales", response_model=bool)
async def agregar_material_a_producto(
    producto_id: str,
    material: dict = Body(...),
    product_service: ProductService = Depends(get_product_service)
):
    """
    Agregar un material a un producto existente.
    """
    try:
        ok = await product_service.add_material_to_product(producto_id, material)
        if not ok:
            raise HTTPException(status_code=404, detail="Producto no encontrado o sin cambios")
        return ok
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/categorias", response_model=str, status_code=201)
async def crear_categoria(
    categoria: str = Body(..., embed=True),
    product_service: ProductService = Depends(get_product_service)
):
    """
    Crear una nueva categoría (producto vacío).
    """
    try:
        categoria_id = await product_service.create_category(categoria)
        return categoria_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/trabajadores", response_model=str, status_code=201)
async def crear_trabajador(
    ci: str = Body(..., embed=True),
    nombre: str = Body(..., embed=True),
    contrasena: str = Body(default=None, embed=True),
    worker_service: WorkerService = Depends(get_worker_service)
):
    """
    Crear un nuevo trabajador (opcionalmente con contraseña).
    """
    try:
        worker_id = await worker_service.create_worker(ci, nombre, contrasena)
        return worker_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trabajadores/buscar", response_model=List[Trabajador])
async def buscar_trabajadores(
    nombre: str = Query(..., description="Nombre a buscar"),
    worker_service: WorkerService = Depends(get_worker_service)
):
    """
    Buscar trabajadores por nombre (case-insensitive).
    """
    try:
        return await worker_service.search_workers_by_name(nombre)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/jefes_brigada", response_model=str, status_code=201)
async def crear_jefe_brigada(
    ci: str = Body(..., embed=True),
    nombre: str = Body(..., embed=True),
    contrasena: str = Body(..., embed=True),
    integrantes: list = Body(default=None),
    brigada_repo: BrigadaRepository = Depends(get_brigada_repository),
    worker_service: WorkerService = Depends(get_worker_service)
):
    """
    Crear un jefe de brigada (trabajador con contraseña) y asignar brigada (con o sin integrantes).
    """
    try:
        # Crear trabajador con contraseña
        await worker_service.create_worker(ci, nombre, contrasena)
        integrantes_ci = [i["CI"] for i in integrantes] if integrantes else []
        brigada_id = brigada_repo.create_brigada(ci, integrantes_ci)
        return brigada_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/trabajadores/{ci}/convertir_jefe", response_model=bool)
async def convertir_trabajador_a_jefe(
    ci: str,
    contrasena: str = Body(..., embed=True),
    integrantes: list = Body(default=None),
    brigada_repo: BrigadaRepository = Depends(get_brigada_repository),
    worker_service: WorkerService = Depends(get_worker_service)
):
    """
    Convertir un trabajador existente en jefe de brigada (asignar contraseña y crear brigada donde sea líder).
    """
    try:
        ok = await worker_service.set_worker_password(ci, contrasena)
        integrantes_ci = [i["CI"] for i in integrantes] if integrantes else []
        brigada_repo.create_brigada(ci, integrantes_ci)
        return ok
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/trabajadores/asignar_brigada", response_model=bool, status_code=201)
async def crear_trabajador_y_asignar_brigada(
    ci: str = Body(..., embed=True),
    nombre: str = Body(..., embed=True),
    brigada_id: str = Body(..., embed=True),
    contrasena: str = Body(default=None, embed=True),
    worker_service: WorkerService = Depends(get_worker_service),
    brigada_repo: BrigadaRepository = Depends(get_brigada_repository)
):
    """
    Crear un trabajador y asignarlo a una brigada existente en un solo paso.
    """
    try:
        # Crear trabajador
        await worker_service.create_worker(ci, nombre, contrasena)
        # Asignar a brigada
        ok = brigada_repo.add_trabajador(brigada_id, ci)
        return ok
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clientes", response_model=Cliente, status_code=201)
async def crear_cliente(
    cliente_request: ClienteCreateRequest,
    client_service: ClientService = Depends(get_client_service)
):
    """
    Crear un nuevo cliente o actualizar si ya existe basado en el número de cliente.
    Si el número de cliente no existe, crea el cliente completo.
    Si ya existe, actualiza los demás datos.
    """
    try:
        # Convertir el request a la entidad Cliente
        cliente = Cliente(
            numero=cliente_request.numero,
            nombre=cliente_request.nombre,
            direccion=cliente_request.direccion,
            latitud=cliente_request.latitud,
            longitud=cliente_request.longitud
        )
        
        # Crear o actualizar el cliente
        cliente_creado = await client_service.create_or_update_client(cliente)
        return cliente_creado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/clientes/{numero}/verificar", response_model=dict)
async def verificar_cliente_por_numero(
    numero: str,
    client_service: ClientService = Depends(get_client_service)
):
    """
    Verificar si existe un cliente por número y retornar solo nombre y dirección si existe.
    """
    try:
        cliente = await client_service.find_client_by_number(numero)
        
        if cliente:
            return {
                "existe": True,
                "nombre": cliente.nombre,
                "direccion": cliente.direccion
            }
        else:
            return {
                "existe": False,
                "mensaje": f"No se encontró un cliente con el número {numero}"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/clientes", summary="Listar clientes", tags=["Clientes"], response_model=List[dict])
def listar_clientes(
    numero: Optional[str] = Query(None, description="Número de cliente"),
    nombre: Optional[str] = Query(None, description="Nombre del cliente (búsqueda parcial)"),
    direccion: Optional[str] = Query(None, description="Dirección del cliente (búsqueda parcial)"),
    client_service: ClientService = Depends(get_client_service)
):
    """Listar clientes con filtros opcionales."""
    clientes = client_service.get_clientes(numero, nombre, direccion)
    return clientes


@router.post("/clientes/simple", response_model=Cliente, status_code=201)
async def crear_cliente_simple(
    cliente_request: ClienteCreateSimpleRequest,
    client_service: ClientService = Depends(get_client_service)
):
    """
    Crear un nuevo cliente con solo los campos obligatorios (numero, nombre, direccion).
    Los campos latitud y longitud son opcionales.
    """
    try:
        # Convertir el request a la entidad Cliente
        cliente = Cliente(
            numero=cliente_request.numero,
            nombre=cliente_request.nombre,
            direccion=cliente_request.direccion,
            latitud=cliente_request.latitud or "",
            longitud=cliente_request.longitud or ""
        )
        
        # Crear o actualizar el cliente
        cliente_creado = await client_service.create_or_update_client(cliente)
        return cliente_creado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
