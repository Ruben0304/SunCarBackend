from typing import List
from domain.entities.form import Form
from infrastucture.repositories.formularios_repository import FormRepository


class FormService:
    def __init__(self, form_repository: FormRepository):
        self._form_repository = form_repository

    def save_form(self, form_data: dict) -> str:
        return self._form_repository.save_form(form_data)

    async def get_all_forms(self) -> List[Form]:
        return  self._form_repository.get_all_forms()

    def get_reportes(self, tipo_reporte=None, cliente_numero=None, fecha_inicio=None, fecha_fin=None, lider_ci=None, descripcion=None, q=None):
        return self._form_repository.get_reportes(tipo_reporte, cliente_numero, fecha_inicio, fecha_fin, lider_ci, descripcion, q)

    def get_reportes_view(self, tipo_reporte=None, cliente_numero=None, fecha_inicio=None, fecha_fin=None, lider_ci=None):
        return self._form_repository.get_reportes_view(tipo_reporte, cliente_numero, fecha_inicio, fecha_fin, lider_ci)