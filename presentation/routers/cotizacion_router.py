from fastapi import APIRouter, HTTPException

from application.services.cotizacion_service import CotizacionService
from presentation.schemas.requests.CotizacionRequest import CotizacionRequest

router = APIRouter()


@router.post("/cotizacion")
async def crear_cotizacion(request: CotizacionRequest):
    """
    Endpoint para crear una nueva cotización.
    Recibe un mensaje y lo muestra en consola.
    """
    try:
        # Crear instancia del service
        cotizacion_service = CotizacionService()
        
        # Procesar la cotización
        resultado = await cotizacion_service.procesar_cotizacion(request.mensaje)
        
        if resultado["success"]:
            return {
                "success": True,
                "message": resultado["message"],
                "mensaje_recibido": resultado["mensaje_recibido"]
            }
        else:
            raise HTTPException(status_code=500, detail=resultado["message"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}") 