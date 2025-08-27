import os
from typing import Optional
from infrastucture.external_services.gemini_provider import GeminiProvider


class ChatService:
    def __init__(self, gemini_provider: GeminiProvider):
        self.gemini_provider = gemini_provider
        self.default_model = os.getenv("GEMINI_DEFAULT_MODEL", "gemini-1.5-flash")
        self.system_prompt = """Eres un asistente inteligente de SunCar, una empresa especializada en energía solar. 
Tu función es ayudar a los usuarios con consultas relacionadas con:
- Instalaciones de paneles solares
- Mantenimiento de sistemas solares
- Consultas técnicas sobre energía solar
- Información sobre productos y servicios de la empresa
- Resolución de problemas técnicos

Responde de manera profesional, clara y útil. Si no tienes información específica sobre algo, 
indícalo claramente y sugiere alternativas o recomienda contactar con el equipo técnico."""

    async def chat(self, user_message: str, custom_system_prompt: Optional[str] = None, 
                   model: Optional[str] = None, streaming: bool = False) -> str:
        """
        Procesa un mensaje del usuario y devuelve una respuesta del LLM
        
        Args:
            user_message: Mensaje del usuario
            custom_system_prompt: Prompt del sistema personalizado (opcional)
            model: Modelo a usar (opcional, por defecto gemini-1.5-flash)
            streaming: Si usar streaming o no
            
        Returns:
            Respuesta del LLM
        """
        used_model = model or self.default_model
        used_system_prompt = custom_system_prompt or self.system_prompt
        
        return await self.gemini_provider.chat(
            model=used_model,
            prompt=user_message,
            system_prompt=used_system_prompt,
            streaming=streaming
        )