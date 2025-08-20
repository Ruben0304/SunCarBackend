import os
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from application.services.auth_service import AuthService
from application.services.worker_service import WorkerService
from infrastucture.dependencies import get_auth_service, get_worker_service
from presentation.schemas.responses import LoginResponse, ChangePasswordResponse

router = APIRouter()


class LoginRequest(BaseModel):
    ci: str
    contraseña: str


class ChangePasswordRequest(BaseModel):
    ci: str
    nueva_contrasena: str


class TokenLoginRequest(BaseModel):
    usuario: str
    contrasena: str


class TokenResponse(BaseModel):
    success: bool
    message: str
    token: str = None


@router.post("/login", response_model=LoginResponse)
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


@router.post("/cambiar_contrasena", response_model=ChangePasswordResponse)
async def cambiar_contrasena(
    data: ChangePasswordRequest,
    worker_service: WorkerService = Depends(get_worker_service)
):
    """
    Cambia la contraseña de un trabajador dado el CI y la nueva contraseña.
    """
    try:
        ok = await worker_service.set_worker_password(data.ci, data.nueva_contrasena)
        if not ok:
            return ChangePasswordResponse(
                success=False,
                message="Trabajador no encontrado o sin cambios"
            )
        return ChangePasswordResponse(
            success=True,
            message="Contraseña cambiada exitosamente"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login-token", response_model=TokenResponse)
async def login_token(credentials: TokenLoginRequest):
    """
    Endpoint para obtener el token de autorización usando credenciales hardcodeadas.
    Usuario: admin, Contraseña: admin123
    """
    # Credenciales hardcodeadas
    ADMIN_USER = "admin"
    ADMIN_PASSWORD = "admin123"
    
    if credentials.usuario == ADMIN_USER and credentials.contrasena == ADMIN_PASSWORD:
        token = os.getenv("AUTH_TOKEN", "suncar-token-2025")
        return TokenResponse(
            success=True,
            message="Login exitoso",
            token=token
        )
    else:
        return TokenResponse(
            success=False,
            message="Credenciales incorrectas",
            token=None
        )


@router.get("/validate")
async def validate_token():
    """
    Endpoint para validar el token de autorización.
    Si el middleware permite llegar aquí, el token es válido.
    """
    return {
        "success": True,
        "message": "Token válido",
        "token": os.getenv("AUTH_TOKEN", "suncar-token-2025")
    } 