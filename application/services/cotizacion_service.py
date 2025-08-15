from typing import Optional
from .email_service import EmailService


class CotizacionService:
    def __init__(self):
        self.email_service = EmailService()

    async def procesar_cotizacion(self, mensaje: str) -> dict:
        """
        Procesa una cotización recibiendo un mensaje, lo muestra en consola y envía por correo.
        
        Args:
            mensaje (str): El mensaje de la cotización
            
        Returns:
            dict: Respuesta con el estado del procesamiento
        """
        try:
            # Mostrar el mensaje en consola
            print(f"=== COTIZACIÓN RECIBIDA ===")
            print(f"Mensaje: {mensaje}")
            print(f"==========================")
            
            # Enviar por correo electrónico
            email_result = await self.email_service.enviar_cotizacion(mensaje)
            
            return {
                "success": True,
                "message": "Cotización procesada exitosamente",
                "mensaje_recibido": mensaje,
                "email_enviado": email_result["success"],
                "email_mensaje": email_result["message"],
                "destinatario": email_result.get("destinatario")
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error al procesar cotización: {str(e)}",
                "mensaje_recibido": None,
                "email_enviado": False,
                "email_mensaje": f"Error: {str(e)}"
            } 