from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    message: str = Field(..., description="Mensaje del usuario", min_length=1, max_length=5000)
    model: Optional[str] = Field(None, description="Modelo de IA a usar (opcional, por defecto gemini-1.5-flash)")
    system_prompt: Optional[str] = Field(None, description="Prompt del sistema personalizado (opcional)")
    streaming: bool = Field(False, description="Si usar streaming o no")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "¿Cómo puedo mejorar la eficiencia de mis paneles solares?",
                "model": "gemini-1.5-flash",
                "system_prompt": None,
                "streaming": False
            }
        }
    }