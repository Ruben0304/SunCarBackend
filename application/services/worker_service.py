# application/services/worker_service.py
from typing import List
from fastapi import Depends

from domain.entities.trabajador import Trabajador
from infrastucture.dependencies import get_workers_repository
from infrastucture.repositories.trabajadores_repository import WorkerRepository


class WorkerService:
    def __init__(self, worker_repo: WorkerRepository):
        self.worker_repo = worker_repo

    async def get_all_workers(self) -> List[Trabajador]:
        """
        Obtains all workers.
        """
        return await self.worker_repo.get_all_workers()

# Function to get the service instance (dependency injection for FastAPI)
def get_worker_service(
        worker_repo: WorkerRepository = Depends(get_workers_repository)
) -> WorkerService:
    """
    Dependency for FastAPI that returns the WorkerService instance.
    """
    return WorkerService(worker_repo)