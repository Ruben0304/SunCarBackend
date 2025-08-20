import os
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

AUTH_TOKEN = os.getenv("AUTH_TOKEN", "suncar-token-2025")

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Rutas excluidas de autenticación
        excluded_paths = [
            "/docs",
            "/redoc", 
            "/openapi.json",
            "/api/auth/login",
            "/api/auth/login-token",
            "/",
            "/favicon.ico"
        ]
        
        # Verificar si la ruta está excluida
        if request.url.path in excluded_paths:
            return await call_next(request)
        
        # Verificar token en header Authorization
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Token de autorización requerido"}
            )
        
        token = auth_header.replace("Bearer ", "")
        if token != AUTH_TOKEN:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Token inválido"}
            )
        
        return await call_next(request)