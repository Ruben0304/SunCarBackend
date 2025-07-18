from typing import Annotated  # Recommended for clearer type hinting in FastAPI
from fastapi import Depends

from application.services.client_service import ClientService
from application.services.product_service import ProductService
from application.services.worker_service import WorkerService
from application.services.form_service import FormService
from application.services.auth_service import AuthService
from application.services.update_service import UpdateService
from infrastucture.repositories.adjuntos_repository import AdjuntosRepository
from application.services.brigada_service import BrigadaService
from infrastucture.repositories.client_repository import ClientRepository
from infrastucture.repositories.productos_repository import ProductRepository
from infrastucture.repositories.trabajadores_repository import WorkerRepository
from infrastucture.repositories.reportes_repository import FormRepository  # Nota el plural "repositories"
from infrastucture.repositories.brigada_repository import BrigadaRepository

# Global singleton instances for repositories
product_repository = ProductRepository()
worker_repository = WorkerRepository()
form_repository = FormRepository()
brigada_repository = BrigadaRepository()
client_repository = ClientRepository()
adjuntos_repository = AdjuntosRepository()


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

def get_client_repository() -> ClientRepository:
    return client_repository




def get_brigada_repository() -> BrigadaRepository:
    """
    Dependency for FastAPI that returns the singleton instance of BrigadaRepository.
    """
    return brigada_repository

def get_adjuntos_repository() -> AdjuntosRepository:
    """
    Dependency for FastAPI that returns the singleton instance of BrigadaRepository.
    """
    return adjuntos_repository

# Dependency functions for services
def get_product_service(
        product_repo: Annotated[ProductRepository, Depends(get_product_repository)]
) -> ProductService:
    """
    Dependency for FastAPI that returns an instance of ProductService.
    """
    return ProductService(product_repo)


def get_worker_service(
        worker_repo: Annotated[WorkerRepository, Depends(get_worker_repository)],
        brigada_repo: Annotated[BrigadaRepository, Depends(get_brigada_repository)]
) -> WorkerService:
    """
    Dependency for FastAPI that returns an instance of WorkerService.
    """
    return WorkerService(worker_repo, brigada_repo)


def get_form_service(
        form_repo: Annotated[FormRepository, Depends(get_form_repository)],
        adjuntos_repo: Annotated[AdjuntosRepository, Depends(get_adjuntos_repository)]
) -> FormService:
    return FormService(form_repo,adjuntos_repo)

def get_client_service(
        client_repo: Annotated[ClientRepository, Depends(get_client_repository)]
) -> ClientService:
    return ClientService(client_repo)



def get_auth_service(
        worker_repo: Annotated[WorkerRepository, Depends(get_worker_repository)],
        brigada_repo: Annotated[BrigadaRepository, Depends(get_brigada_repository)]
) -> AuthService:
    """
    Dependency for FastAPI that returns an instance of AuthService.
    """
    return AuthService(worker_repo, brigada_repo)


def get_update_service(
        product_service: Annotated[ProductService, Depends(get_product_service)],
        worker_service: Annotated[WorkerService, Depends(get_worker_service)],
        client_service: Annotated[ClientService, Depends(get_client_service)]
) -> UpdateService:
    """
    Dependency for FastAPI that returns an instance of UpdateService.
    """
    return UpdateService(product_service, worker_service, client_service)


def get_brigada_service(
        brigada_repo: Annotated[BrigadaRepository, Depends(get_brigada_repository)]
) -> BrigadaService:
    """
    Dependency for FastAPI that returns an instance of BrigadaService.
    """
    return BrigadaService(brigada_repo)
