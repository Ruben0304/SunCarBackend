from typing import List, Optional
from infrastucture.repositories.brigada_repository import BrigadaRepository
from domain.entities.brigada import Brigada


class BrigadaService:
    def __init__(self, brigada_repo: BrigadaRepository):
        self.brigada_repo = brigada_repo

    async def delete_brigada(self, brigada_id: str) -> bool:
        """
        Elimina una brigada por su ID.
        """
        return self.brigada_repo.delete_brigada(brigada_id)

    async def remove_worker_from_brigada(self, brigada_id: str, trabajador_ci: str) -> bool:
        """
        Elimina un trabajador de una brigada específica.
        """
        return self.brigada_repo.remove_trabajador(brigada_id, trabajador_ci)

    async def get_brigada_by_lider_ci(self, lider_ci: str) -> Optional[Brigada]:
        """
        Obtiene una brigada por el CI de su líder.
        """
        return self.brigada_repo.get_brigada_by_lider_ci(lider_ci)

    async def get_all_brigadas(self) -> List[Brigada]:
        """
        Obtiene todas las brigadas.
        """
        return self.brigada_repo.get_all_brigadas() 