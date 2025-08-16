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
    
    async def enviar_cotizacion(self, mensaje: str, destinatario: str = None, latitud: Optional[float] = None, longitud: Optional[float] = None) -> dict:
        """
        Envía una cotización por correo electrónico.
        
        Args:
            mensaje (str): El mensaje de la cotización
            destinatario (str): Email del destinatario (por defecto usa el hardcodeado)
            latitud (Optional[float]): Latitud de la ubicación para mostrar mapa
            longitud (Optional[float]): Longitud de la ubicación para mostrar mapa
            
        Returns:
            dict: Respuesta con el estado del envío
        """
        try:
            # Email hardcodeado por el momento (después vendrá de la BD)
            if not destinatario:
                destinatario = "hernandzruben9@gmail.com"  # Email hardcodeado
            
            # Generar contenido del mapa si hay coordenadas
            mapa_html = ""
            if latitud is not None and longitud is not None:
                mapa_html = f"""
                    <div style="margin: 20px 0;">
                        <h3>Ubicación:</h3>
                        <p><strong>Coordenadas:</strong> {latitud}, {longitud}</p>
                        <div style="text-align: center; margin: 10px 0;">
                            <img src="https://maps.googleapis.com/maps/api/staticmap?center={latitud},{longitud}&zoom=15&size=400x300&markers=color:red%7C{latitud},{longitud}&key=AIzaSyBvOkBwgGlbUNt0H_rBpyHay4ZWqQhiMjE" 
                                 alt="Mapa de ubicación" 
                                 style="max-width: 100%; height: auto; border: 1px solid #ccc;">
                        </div>
                        <p style="text-align: center;">
                            <a href="https://www.google.com/maps?q={latitud},{longitud}" target="_blank" 
                               style="color: #1a73e8; text-decoration: none;">
                                Ver en Google Maps
                            </a>
                        </p>
                    </div>
                """
            
            # Crear el mensaje
            message = MessageSchema(
                subject="Nueva Cotización Recibida - SunCar",
                recipients=[destinatario],
                body=f"""
                <html>
                <body>
                    <h2>Nueva Cotización Recibida</h2>
                    <p><strong>Mensaje:</strong></p>
                    <p>{mensaje.replace(chr(10), '<br>')}</p>
                    {mapa_html}
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