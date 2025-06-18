# Instancia singleton del repositorio
from infrastucture.repositories.productos_repository import ProductRepository
from infrastucture.repositories.trabajadores_repository import WorkerRepository

product_repository = ProductRepository()
worker_repository = WorkerRepository()


# Función para obtener la instancia (dependency injection para FastAPI)
def get_productos_repository() -> ProductRepository:
    """
    Dependency para FastAPI que devuelve la instancia singleton del repositorio
    """
    return product_repository

def get_workers_repository() -> WorkerRepository:
    return worker_repository