from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from presentation.middleware.auth_middleware import AuthMiddleware

from presentation.routers.auth_router import router as auth_router
from presentation.routers.trabajadores_router import router as trabajadores_router
from presentation.routers.brigadas_router import router as brigadas_router
from presentation.routers.clientes_router import router as clientes_router
from presentation.routers.productos_router import router as productos_router
from presentation.routers.reportes_router import router as reportes_router
from presentation.routers.updates_router import router as updates_router
from presentation.routers.admin_router import router as admin_router
from presentation.routers.shared_router import router as shared_router
from presentation.routers.pdf_router import router as pdf_router
from presentation.routers.cotizacion_router import router as cotizacion_router

from dotenv import load_dotenv
from presentation.handlers.validation_exception_handler import validation_exception_handler

app = FastAPI(
    title="SunCar Backend",
    description="API con arquitectura limpia de la empresa SunCar",
    version="1.0.0"
)

# Cargar variables de entorno del archivo .env
load_dotenv()

app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.add_middleware(AuthMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Solo permite este origen
    allow_credentials=True,  # Permite el envío de credenciales
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los encabezados
)
# Incluir los routers organizados por features
app.include_router(
    auth_router,
    prefix="/api/auth",
    tags=["Autenticación"]
)

app.include_router(
    trabajadores_router,
    prefix="/api/trabajadores",
    tags=["Trabajadores"]
)

app.include_router(
    brigadas_router,
    prefix="/api/brigadas",
    tags=["Brigadas"]
)

app.include_router(
    clientes_router,
    prefix="/api/clientes",
    tags=["Clientes"]
)

app.include_router(
    productos_router,
    prefix="/api/productos",
    tags=["Productos"]
)

app.include_router(
    reportes_router,
    prefix="/api/reportes",
    tags=["Reportes"]
)

app.include_router(
    updates_router,
    prefix="/api/update",
    tags=["Actualizaciones"]
)

app.include_router(
    admin_router,
    prefix="/api/admin",
    tags=["Administración"]
)

app.include_router(
    shared_router,
    prefix="/api",
    tags=["Compartidos"]
)

app.include_router(
    pdf_router,
    prefix="/api/pdf",
    tags=["PDF"]
)

app.include_router(
    cotizacion_router,
    prefix="/api",
    tags=["Cotizaciones"]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )

