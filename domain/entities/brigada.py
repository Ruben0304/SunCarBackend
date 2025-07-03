from typing import List, Optional

from pydantic import BaseModel

from domain.entities.trabajador import Trabajador


class Brigada(BaseModel):
    id: Optional[str] = None
    lider: Trabajador
    integrantes: List[Trabajador]