from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    def __init__(self):
        # Configuración del servidor de correo (Gmail con datos reales)
        self.config = ConnectionConfig(
            MAIL_USERNAME=os.getenv("MAIL_USERNAME", "rubianclaude@gmail.com"),
            MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
            MAIL_FROM=os.getenv("MAIL_FROM", "rubianclaude@gmail.com"),
            MAIL_PORT=587,
            MAIL_SERVER="smtp.gmail.com",
            MAIL_FROM_NAME="SunCar Sistema",
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True
        )
        self.fastmail = FastMail(self.config)
    
    async def enviar_cotizacion(self, mensaje: str, destinatario: str = None) -> dict:
        """
        Envía una cotización por correo electrónico.
        
        Args:
            mensaje (str): El mensaje de la cotización
            destinatario (str): Email del destinatario (por defecto usa el hardcodeado)
            
        Returns:
            dict: Respuesta con el estado del envío
        """
        try:
            # Email hardcodeado por el momento (después vendrá de la BD)
            if not destinatario:
                destinatario = "hernandzruben9@gmail.com"  # Email hardcodeado
            
            # Crear el mensaje
            message = MessageSchema(
                subject="Nueva Cotización Recibida - SunCar",
                recipients=[destinatario],
                body=f"""
                <html>
                <body>
                    <h2>Nueva Cotización Recibida</h2>
                    <p><strong>Mensaje:</strong></p>
                    <p>{mensaje}</p>
                    <br>
                    <p>Este es un mensaje automático del sistema SunCar.</p>
                    <p><small>Enviado desde: rubianclaude@gmail.com</small></p>
                </body>
                </html>
                """,
                subtype="html"
            )
            
            # Enviar el correo
            await self.fastmail.send_message(message)
            
            return {
                "success": True,
                "message": f"Correo enviado exitosamente a {destinatario}",
                "destinatario": destinatario
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error al enviar correo: {str(e)}",
                "destinatario": destinatario
            } 