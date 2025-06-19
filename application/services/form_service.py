from typing import List
from domain.entities.form import Form
from infrastucture.repositories.formularios_repository import FormRepository


class FormService:
    def __init__(self, form_repository: FormRepository):
        self._form_repository = form_repository

    async def get_all_forms(self) -> List[Form]:
        return await self._form_repository.get_all_forms() 