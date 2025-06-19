from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from domain.entities.producto import Material
from domain.entities.trabajador import Trabajador


class Location(BaseModel):
    address: str
    latitude: float
    longitude: float


class Form(BaseModel):
    id: str = None
    service_type: str
    # brigade_chief: Trabajador
    # brigade_members: List[Trabajador]
    # work_date_ini: datetime
    # work_date_fin: datetime
    # materials: List[Material]
    # location: Location
    # photos: List[str]
