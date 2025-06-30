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

app = FastAPI(
    title="SunCar Backend",
    description="API con arquitectura limpia de la empresa SunCar",
    version="1.0.0"
)

# Cargar variables de entorno del archivo .env
load_dotenv()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Construir un mensaje detallado
    errors = []
    for err in exc.errors():
        loc = " -> ".join(str(l) for l in err['loc'])
        msg = err['msg']
        value = err.get('ctx', {}).get('limit_value', None)
        errors.append({
            "field": loc,
            "error": msg,
            "value": err.get('input', None)  # input es el valor recibido (FastAPI 0.100+)
        })
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Error de validación en los datos enviados",
            "errors": errors
        }
    )

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



