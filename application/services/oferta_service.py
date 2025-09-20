from typing import List, Optional

from domain.entities.oferta import Oferta, OfertaSimplificada
from infrastucture.repositories.ofertas_repository import OfertasRepository


class OfertaService:
    def __init__(self, ofertas_repository: OfertasRepository):
        self.ofertas_repository = ofertas_repository

    async def get_all(self) -> List[Oferta]:
        return self.ofertas_repository.get_all()

    async def get_all_simplified(self) -> List[OfertaSimplificada]:
        ofertas = self.ofertas_repository.get_all()
        return [
            OfertaSimplificada(
                id=oferta.id,
                descripcion=oferta.descripcion,
                precio=oferta.precio,
                precio_cliente=oferta.precio_cliente,
                imagen=oferta.imagen
            )
            for oferta in ofertas
        ]

    async def get_by_id(self, oferta_id: str) -> Optional[Oferta]:
        return self.ofertas_repository.get_by_id(oferta_id)

    async def create(self, oferta: Oferta | dict) -> str:
        if not isinstance(oferta, Oferta):
            oferta = Oferta(**oferta)
        return self.ofertas_repository.create(oferta)

    async def update(self, oferta_id: str, new_data: dict) -> bool:
        return self.ofertas_repository.update(oferta_id, new_data)

    async def delete(self, oferta_id: str) -> bool:
        return self.ofertas_repository.delete(oferta_id)

    async def add_elemento(self, oferta_id: str, elemento_data: dict) -> bool:
        return self.ofertas_repository.add_elemento(oferta_id, elemento_data)

    async def remove_elemento(self, oferta_id: str, elemento_index: int) -> bool:
        return self.ofertas_repository.remove_elemento(oferta_id, elemento_index)

    async def update_elemento(self, oferta_id: str, elemento_index: int, nuevos_datos: dict) -> bool:
        return self.ofertas_repository.update_elemento(oferta_id, elemento_index, nuevos_datos)


