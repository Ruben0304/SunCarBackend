from typing import List, Optional

from pydantic import BaseModel

from domain.entities.trabajador import Trabajador


class Brigada(BaseModel):
    lider_ci: str
    lider: Trabajador
    integrantes: List[Trabajador]