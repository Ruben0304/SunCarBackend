from typing import List

from fastapi import APIRouter, Depends
from domain.entities.form import Form
from application.services.form_service import FormService
from infrastucture.dependencies import get_form_service

router = APIRouter()


