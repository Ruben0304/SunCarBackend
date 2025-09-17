from typing import Optional, List
from pydantic import BaseModel
from domain.entities.lead import Lead


class LeadCreateResponse(BaseModel):
    success: bool
    message: str
    data: Lead


class LeadGetResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Lead] = None


class LeadListResponse(BaseModel):
    success: bool
    message: str
    data: List[Lead]


class LeadUpdateResponse(BaseModel):
    success: bool
    message: str
    data: Lead


class LeadDeleteResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None