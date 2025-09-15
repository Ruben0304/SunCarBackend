import logging
from typing import Annotated, AsyncGenerator
import json

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

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
    # Si es streaming, redirigir al endpoint de streaming
    if chat_request.streaming:
        return await chat_streaming(chat_request, chat_service)
    
    try:
        response = await chat_service.chat(
            user_message=chat_request.message,
            custom_system_prompt=chat_request.system_prompt,
            model=chat_request.model,
            streaming=False
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


@router.post("/stream", tags=["Chat"])
async def chat_streaming(
    chat_request: ChatRequest,
    chat_service: Annotated[ChatService, Depends(get_chat_service)]
):
    """
    Enviar un mensaje al LLM y recibir una respuesta en streaming (Server-Sent Events).
    
    Este endpoint permite recibir la respuesta del LLM de manera progresiva
    usando Server-Sent Events (SSE) para una mejor experiencia de usuario.
    """
    async def generate_response() -> AsyncGenerator[str, None]:
        try:
            model_used = chat_request.model or "gemini-1.5-flash"
            
            # Enviar metadata inicial
            yield f"data: {json.dumps({'type': 'start', 'model': model_used})}\n\n"
            
            # Obtener respuesta streaming del servicio
            async for chunk in chat_service.chat_stream(
                user_message=chat_request.message,
                custom_system_prompt=chat_request.system_prompt,
                model=chat_request.model
            ):
                yield f"data: {json.dumps({'type': 'content', 'data': chunk})}\n\n"
            
            # Enviar señal de finalización
            yield f"data: {json.dumps({'type': 'end'})}\n\n"
            
        except Exception as e:
            logger.error(f"Error en chat_streaming: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    
    return StreamingResponse(
        generate_response(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*"
        }
    )