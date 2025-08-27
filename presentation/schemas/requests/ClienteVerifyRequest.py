from pydantic import BaseModel


class ClienteVerifyRequest(BaseModel):
    identifier: str  # Puede ser numero de telefono o numero de cliente