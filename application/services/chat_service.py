import os
from typing import Optional, AsyncGenerator
from infrastucture.external_services.gemini_provider import GeminiProvider


class ChatService:
    def __init__(self, gemini_provider: GeminiProvider):
        self.gemini_provider = gemini_provider
        self.default_model = os.getenv("GEMINI_DEFAULT_MODEL", "gemini-1.5-flash")
        self.system_prompt = ""

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
    
    async def chat_stream(self, user_message: str, custom_system_prompt: Optional[str] = None, 
                         model: Optional[str] = None) -> AsyncGenerator[str, None]:
        """
        Procesa un mensaje del usuario y devuelve una respuesta del LLM en streaming
        
        Args:
            user_message: Mensaje del usuario
            custom_system_prompt: Prompt del sistema personalizado (opcional)
            model: Modelo a usar (opcional, por defecto gemini-1.5-flash)
            
        Yields:
            Chunks de texto de la respuesta del LLM
        """
        used_model = model or self.default_model
        used_system_prompt = custom_system_prompt or self.system_prompt
        
        async for chunk in self.gemini_provider.chat_stream(
            model=used_model,
            prompt=user_message,
            system_prompt=used_system_prompt
        ):
            yield chunk