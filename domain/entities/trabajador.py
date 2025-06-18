from pydantic import BaseModel


class Trabajador(BaseModel):
    id: str = None  # Se mapea desde _id de MongoDB
    CI: str
    nombre: str