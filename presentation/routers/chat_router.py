import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from application.services.chat_service import ChatService
from infrastucture.dependencies import get_chat_service
from presentation.schemas.requests.ChatRequest import ChatRequest
from presentation.schemas.responses.chat_responses import ChatResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=ChatResponse, tags=["Chat"])
async def chat_with_llm(
    chat_request: ChatRequest,
    chat_service: Annotated[ChatService, Depends(get_chat_service)]
):
    """
    Enviar un mensaje al LLM y recibir una respuesta.
    
    Este endpoint permite interactuar con el asistente inteligente de SunCar
    para obtener información sobre energía solar, productos y servicios.
    """
    try:
        response = await chat_service.chat(
            user_message=chat_request.message,
            custom_system_prompt=chat_request.system_prompt,
            model=chat_request.model,
            streaming=chat_request.streaming
        )
        
        model_used = chat_request.model or "gemini-1.5-flash"
        
        return ChatResponse(
            success=True,
            message="Respuesta generada exitosamente",
            response=response,
            model_used=model_used
        )
        
    except Exception as e:
        logger.error(f"Error en chat_with_llm: {e}", exc_info=True)
        return ChatResponse(
            success=False,
            message=f"Error al procesar el mensaje: {str(e)}",
            response="",
            model_used=""
        )