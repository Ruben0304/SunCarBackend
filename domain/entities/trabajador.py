from pydantic import BaseModel
from typing import Optional


class Trabajador(BaseModel):
    CI: str
    nombre: str


