from typing import List

from fastapi import APIRouter, Depends
from domain.entities.form import Form
from application.services.form_service import FormService
from infrastucture.dependencies import get_form_service

router = APIRouter()


@router.get("/forms", response_model=List[Form])
async def get_all_forms(
        form_service: FormService = Depends(get_form_service)
) -> List[Form]:
    forms = await form_service.get_all_forms()
    return forms
