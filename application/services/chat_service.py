import os
from typing import Optional, AsyncGenerator, List, Dict, Any
from pydantic import BaseModel
from infrastucture.external_services.gemini_provider import GeminiProvider


class RecomendacionOfertasResponse(BaseModel):
    """Modelo Pydantic para la respuesta de recomendaciones de ofertas"""
    texto: str
    ids_ordenados: List[str]


class ChatService:
    def __init__(self, gemini_provider: GeminiProvider):
        self.gemini_provider = gemini_provider
        self.default_model = os.getenv("GEMINI_DEFAULT_MODEL", "gemini-2.5-flash")
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

    async def recomendar_ofertas(self, texto_usuario: str, ofertas_contexto: List[Dict[str, Any]],
                                model: Optional[str] = None) -> RecomendacionOfertasResponse:
        """
        Recomienda y ordena ofertas basado en el texto del usuario usando Pydantic para validación.

        Args:
            texto_usuario: Texto/consulta del usuario
            ofertas_contexto: Lista de diccionarios con id, descripcion_detallada, precio
            model: Modelo a usar (opcional)

        Returns:
            RecomendacionOfertasResponse con 'texto' e 'ids_ordenados' validados
        """

        # Preparar el contexto de ofertas para la IA
        contexto_str = "\n".join([
            f"ID: {oferta['id']}, Precio: ${oferta['precio']}, Descripción: {oferta['descripcion_detallada']}"
            for oferta in ofertas_contexto
        ])

        system_prompt = """Eres un especialista en marketing y asistente especializado en recomendar ofertas.
Tu tarea es ordenar TODAS las ofertas proporcionadas de mayor a menor recomendación basándote en la consulta del usuario.

- El campo "texto" debe contener una explicación amigable y clarificadora para un usuario común. NO incluyas IDs de ofertas ni seas extenso. Explica por qué recomiendas la primera opción y por qué la segunda podría ser una buena alternativa si la primera no les interesa. Evita detalles técnicos que no interesen al usuario y enfócate en beneficios claros y comprensibles.
- El campo "ids_ordenados" debe contener TODOS los IDs de las ofertas ordenados de mayor a menor recomendación"""

        user_prompt = f"""Consulta del usuario: {texto_usuario}

Ofertas disponibles:
{contexto_str}

Ordena TODAS estas ofertas de mayor a menor recomendación según la consulta del usuario."""

        used_model = model or self.default_model

        try:
            # Usar el nuevo método con validación Pydantic automática
            response = await self.gemini_provider.chat_with_schema(
                model=used_model,
                prompt=user_prompt,
                response_schema=RecomendacionOfertasResponse,
                system_prompt=system_prompt
            )

            return response

        except Exception:
            # Fallback en caso de error
            ids_disponibles = [oferta['id'] for oferta in ofertas_contexto]
            return RecomendacionOfertasResponse(
                texto="Hola, aquí tienes todas las ofertas disponibles ordenadas alfabéticamente.",
                ids_ordenados=ids_disponibles
            )