from typing import Optional, List
from pydantic import BaseModel
from domain.entities.contacto import Contacto


class ContactoCreateResponse(BaseModel):
    success: bool
    message: str
    data: Contacto


class ContactoUpdateResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Contacto] = None


class ContactoGetResponse(BaseModel):
    success: bool
    message: str
    data: Contacto


class ContactoListResponse(BaseModel):
    success: bool
    message: str
    data: List[Contacto]


class ContactoDeleteResponse(BaseModel):
    success: bool
    message: str
