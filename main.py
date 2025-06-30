from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from presentation.routers.client_router import router as appmovil_router
from presentation.routers.admin_router import router as webadmin_router
from presentation.routers.shared_router import router as compartidos_router
from presentation.routers.reportes_router import router as reportes_router

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Solo permite este origen
    allow_credentials=True,  # Permite el envío de credenciales
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los encabezados
)
# Incluir los routers con prefijos para organizar las rutas
app.include_router(
    appmovil_router,
    prefix="/api",
    tags=["App Móvil"]
)

app.include_router(
    webadmin_router,
    prefix="/api",
    tags=["Web Admin"]
)

app.include_router(
    compartidos_router,
    prefix="/api",
    tags=["Compartidos"]
)

app.include_router(
    reportes_router,
    prefix="/api/reportes",
    tags=["Reportes"]
)



