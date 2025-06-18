from fastapi import APIRouter

router = APIRouter()

# Ruta raíz general
@router.get("/")
async def root():
    return {
        "message": "API con Clean Architecture",
        "endpoints": {
            "mobile": "/api",
            "admin": "/api",
            "shared": "/api"
        }
    }