from fastapi import FastAPI
from presentation.routers.client_router import router as appmovil_router
from presentation.routers.admin_router import router as webadmin_router
from presentation.routers.shared_router import router as compartidos_router

from dotenv import load_dotenv

app = FastAPI(
    title="SunCar Backend",
    description="API con arquitectura limpia de la empresa SunCar",
    version="1.0.0"
)

# Cargar variables de entorno del archivo .env
load_dotenv()

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



