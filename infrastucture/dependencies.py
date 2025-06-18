# Instancia singleton del repositorio
from typing import Annotated # Recommended for clearer type hinting in FastAPI
from fastapi import Depends

from application.services.product_service import ProductService
from application.services.worker_service import WorkerService
from infrastucture.repositories.productos_repository import ProductRepository
from infrastucture.repositories.trabajadores_repository import WorkerRepository


# Global singleton instances for repositories
# It's good practice to make these explicitly global if they are meant to be true singletons
# and instantiated only once when the application starts.
product_repository = ProductRepository()
worker_repository = WorkerRepository()


# Dependency functions for repositories
# These functions act as "providers" for FastAPI's dependency injection system.
# They return the pre-instantiated singleton repository objects.
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


# Dependency functions for services
# These functions demonstrate how to inject repositories into services using Depends.
# Using Annotated[Type, Depends(...)] is the modern and recommended way for clarity.
def get_product_service(
        # FastAPI will automatically resolve get_product_repository and pass its return value
        # to the 'product_repo' parameter.
        product_repo: Annotated[ProductRepository, Depends(get_product_repository)]
) -> ProductService:
    """
    Dependency for FastAPI that returns an instance of ProductService.
    """
    return ProductService(product_repo)

def get_worker_service(
        # Same principle for the WorkerService and WorkerRepository.
        worker_repo: Annotated[WorkerRepository, Depends(get_worker_repository)]
) -> WorkerService:
    """
    Dependency for FastAPI that returns an instance of WorkerService.
    """
    return WorkerService(worker_repo)