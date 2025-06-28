from http.client import HTTPException
from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from application.services.product_service import ProductService
from application.services.worker_service import WorkerService
from application.services.auth_service import AuthService
from application.singleton.brigada_singleton import BrigadaSingleton
from domain.entities.producto import CatalogoProductos, Material, Cataegoria
from domain.entities.trabajador import Trabajador
from domain.entities.brigada import Brigada
from infrastucture.dependencies import get_product_service, get_worker_service, get_auth_service

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
            # Establecer la brigada en el singleton
            BrigadaSingleton.set_brigada_activa(brigada)
            
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


@router.get("/auth/brigada-activa", response_model=Optional[Brigada])
async def get_brigada_activa():
    """
    Endpoint para obtener la brigada activa del singleton.
    Útil para verificar qué brigada está autenticada actualmente.
    """
    try:
        brigada = BrigadaSingleton.get_brigada_activa()
        return brigada
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/auth/logout")
async def logout():
    """
    Endpoint para hacer logout y limpiar la brigada activa del singleton.
    """
    try:
        BrigadaSingleton.clear_brigada_activa()
        return {"success": True, "message": "Logout exitoso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))