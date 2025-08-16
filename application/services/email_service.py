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
                    <div style="margin: 20px 0; padding: 15px; border: 2px solid #e0e0e0; border-radius: 8px; background-color: #f9f9f9;">
                        <h3 style="color: #333; margin-top: 0;">📍 Ubicación de la Cotización</h3>
                        <p><strong>Coordenadas:</strong> {latitud}, {longitud}</p>
                        
                        <div style="background-color: #fff; border: 1px solid #ddd; border-radius: 4px; padding: 10px; margin: 10px 0;">
                            <p style="margin: 5px 0;"><strong>🌐 Latitud:</strong> {latitud}</p>
                            <p style="margin: 5px 0;"><strong>🌐 Longitud:</strong> {longitud}</p>
                        </div>
                        
                        <div style="text-align: center; margin: 15px 0;">
                            <a href="https://www.google.com/maps?q={latitud},{longitud}" target="_blank" 
                               style="display: inline-block; background-color: #1a73e8; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                                🗺️ Ver Ubicación en Google Maps
                            </a>
                        </div>
                        
                        <div style="text-align: center; margin: 10px 0;">
                            <a href="https://maps.apple.com/?q={latitud},{longitud}" target="_blank" 
                               style="display: inline-block; background-color: #007aff; color: white; padding: 8px 16px; text-decoration: none; border-radius: 5px; font-size: 14px; margin: 0 5px;">
                                🍎 Apple Maps
                            </a>
                            <a href="https://www.openstreetmap.org/?mlat={latitud}&mlon={longitud}&zoom=15" target="_blank" 
                               style="display: inline-block; background-color: #7ebc6f; color: white; padding: 8px 16px; text-decoration: none; border-radius: 5px; font-size: 14px; margin: 0 5px;">
                                🌍 OpenStreetMap
                            </a>
                        </div>
                        
                        <p style="font-size: 12px; color: #666; text-align: center; margin-bottom: 0;">
                            Haga clic en cualquier enlace para ver la ubicación en su aplicación de mapas preferida
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