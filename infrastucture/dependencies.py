from typing import Annotated  # Recommended for clearer type hinting in FastAPI
from fastapi import Depends

from application.services.product_service import ProductService
from application.services.worker_service import WorkerService
from application.services.form_service import FormService
from infrastucture.repositories.productos_repository import ProductRepository
from infrastucture.repositories.trabajadores_repository import WorkerRepository
from infrastucture.repositories.formularios_repository import FormRepository  # Nota el plural "repositories"

# Global singleton instances for repositories
product_repository = ProductRepository()
worker_repository = WorkerRepository()
form_repository = FormRepository()


# Dependency functions for repositories
def get_product_repository() -> ProductRepository:
    """
    Dependency for FastAPI that returns the singleton instance of ProductRepository.
    """
    return product_repository


def get_worker_repository() -> WorkerRepository:
    """
    Dependency for FastAPI that returns the singleton instance of WorkerRepository.
    """
    return worker_repository


def get_form_repository() -> FormRepository:
    return form_repository


# Dependency functions for services
def get_product_service(
        product_repo: Annotated[ProductRepository, Depends(get_product_repository)]
) -> ProductService:
    """
    Dependency for FastAPI that returns an instance of ProductService.
    """
    return ProductService(product_repo)


def get_worker_service(
        worker_repo: Annotated[WorkerRepository, Depends(get_worker_repository)]
) -> WorkerService:
    """
    Dependency for FastAPI that returns an instance of WorkerService.
    """
    return WorkerService(worker_repo)


def get_form_service(
        form_repo: Annotated[FormRepository, Depends(get_form_repository)]
) -> FormService:
    return FormService(form_repo)
