from typing import List
from domain.entities.form import Form
from infrastucture.repositories.reportes_repository import FormRepository
from infrastucture.repositories.adjuntos_repository import AdjuntosRepository
from infrastucture.external_services.supabase_uploader import upload_file_to_supabase


class FormService:
    def __init__(self, form_repository: FormRepository, adjuntos_repository: AdjuntosRepository):
        self._form_repository = form_repository
        self._adjuntos_repository = adjuntos_repository

    async def save_form(self, form_data: dict) -> str:
        # Ya no procesamos adjuntos aquí, porque ya son URLs
        return self._form_repository.save_form(form_data)

    async def get_all_forms(self) -> List[Form]:
        return  self._form_repository.get_all_forms()



    def get_reportes(self, tipo_reporte=None, cliente_numero=None, fecha_inicio=None, fecha_fin=None, lider_ci=None, descripcion=None, q=None):
        return self._form_repository.get_reportes(tipo_reporte, cliente_numero, fecha_inicio, fecha_fin, lider_ci, descripcion, q)

    def get_reportes_view(self, tipo_reporte=None, cliente_numero=None, fecha_inicio=None, fecha_fin=None, lider_ci=None):
        return self._form_repository.get_reportes_view(tipo_reporte, cliente_numero, fecha_inicio, fecha_fin, lider_ci)

    def get_reporte_by_id(self, reporte_id: str) -> dict:
        return self._form_repository.get_reporte_by_id(reporte_id)

    def get_materiales_usados_por_brigada(self, lider_ci: str, fecha_inicio: str, fecha_fin: str, categoria: str = None):
        return self._form_repository.get_materiales_usados_por_brigada(lider_ci, fecha_inicio, fecha_fin, categoria)

    def get_materiales_usados_todas_brigadas(self, fecha_inicio: str, fecha_fin: str, categoria: str = None):
        return self._form_repository.get_materiales_usados_todas_brigadas(fecha_inicio, fecha_fin, categoria)