from typing import List
from domain.entities.form import Form
from infrastucture.repositories.reportes_repository import FormRepository


class FormService:
    def __init__(self, form_repository: FormRepository):
        self._form_repository = form_repository

    def save_form(self, form_data: dict) -> str:
        return self._form_repository.save_form(form_data)

    async def get_all_forms(self) -> List[Form]:
        return  self._form_repository.get_all_forms()

    def get_hours_worked_by_ci(self, ci: str, fecha_inicio: str, fecha_fin: str) -> float:
        """
        Obtiene el total de horas trabajadas por una persona dado su CI y rango de fechas.
        
        :param ci: Cédula de identidad de la persona
        :param fecha_inicio: Fecha de inicio del rango (formato: YYYY-MM-DD)
        :param fecha_fin: Fecha de fin del rango (formato: YYYY-MM-DD)
        :return: Total de horas trabajadas
        """
        return self._form_repository.get_hours_worked_by_ci(ci, fecha_inicio, fecha_fin)

    def get_all_workers_hours_worked(self, fecha_inicio: str, fecha_fin: str) -> List[dict]:
        """
        Obtiene todos los trabajadores con sus horas trabajadas en un rango de fechas específico.
        
        :param fecha_inicio: Fecha de inicio del rango (formato: YYYY-MM-DD)
        :param fecha_fin: Fecha de fin del rango (formato: YYYY-MM-DD)
        :return: Lista de trabajadores con sus horas trabajadas
        """
        return self._form_repository.get_all_workers_hours_worked(fecha_inicio, fecha_fin)

    def get_reportes(self, tipo_reporte=None, cliente_numero=None, fecha_inicio=None, fecha_fin=None, lider_ci=None):
        return self._form_repository.get_reportes(tipo_reporte, cliente_numero, fecha_inicio, fecha_fin, lider_ci)

    def get_reportes_view(self, tipo_reporte=None, cliente_numero=None, fecha_inicio=None, fecha_fin=None, lider_ci=None):
        return self._form_repository.get_reportes_view(tipo_reporte, cliente_numero, fecha_inicio, fecha_fin, lider_ci)