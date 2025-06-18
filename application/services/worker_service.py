# application/services/worker_service.py
from typing import List
from fastapi import Depends

from domain.entities.trabajador import Trabajador
from infrastucture.repositories.trabajadores_repository import WorkerRepository


class WorkerService:
    def __init__(self, worker_repo: WorkerRepository):
        self.worker_repo = worker_repo

    async def get_all_workers(self) -> List[Trabajador]:
        """
        Obtains all workers.
        """
        return await self.worker_repo.get_all_workers()

