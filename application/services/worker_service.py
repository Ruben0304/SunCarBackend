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

    def get_hours_worked_by_ci(self, ci: str, fecha_inicio: str, fecha_fin: str) -> float:
        """
        Obtiene el total de horas trabajadas por una persona dado su CI y rango de fechas.
        
        :param ci: Cédula de identidad de la persona
        :param fecha_inicio: Fecha de inicio del rango (formato: YYYY-MM-DD)
        :param fecha_fin: Fecha de fin del rango (formato: YYYY-MM-DD)
        :return: Total de horas trabajadas
        """
        return self.worker_repo.get_hours_worked_by_ci(ci, fecha_inicio, fecha_fin)

    def get_all_workers_hours_worked(self, fecha_inicio: str, fecha_fin: str) -> List[dict]:
        """
        Obtiene todos los trabajadores con sus horas trabajadas en un rango de fechas específico.
        
        :param fecha_inicio: Fecha de inicio del rango (formato: YYYY-MM-DD)
        :param fecha_fin: Fecha de fin del rango (formato: YYYY-MM-DD)
        :return: Lista de trabajadores con sus horas trabajadas
        """
        return self.worker_repo.get_all_workers_hours_worked(fecha_inicio, fecha_fin)

    async def convert_worker_to_leader(self, ci: str, contrasena: str = None, integrantes: list = None) -> bool:
        """
        Convierte un trabajador existente en jefe de brigada:
        - Si no tiene contraseña, se la asigna.
        - Si se pasan integrantes, crea/actualiza la brigada con este trabajador como líder.
        """
        return await self.worker_repo.convert_worker_to_leader(ci, contrasena, integrantes)

    async def create_brigada_leader(self, ci: str, nombre: str, contrasena: str = None, integrantes: list = None) -> str:
        """
        Crea un trabajador (opcionalmente con contraseña) y, si se pasan integrantes, crea la brigada con este trabajador como líder.
        """
        return await self.worker_repo.create_brigada_leader(ci, nombre, contrasena, integrantes)

