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
        return self.worker_repo.get_all_workers()

    async def create_worker(self, ci: str, nombre: str, contrasena: str = None) -> str:
        return self.worker_repo.create_worker(ci, nombre, contrasena)

    async def search_workers_by_name(self, nombre: str) -> list:
        return self.worker_repo.search_workers_by_name(nombre)

    async def set_worker_password(self, ci: str, contrasena: str) -> bool:
        return self.worker_repo.set_worker_password(ci, contrasena)

