from pydantic import BaseModel


class ChatResponse(BaseModel):
    success: bool
    message: str
    response: str = ""
    model_used: str = ""