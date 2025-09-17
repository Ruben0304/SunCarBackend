from typing import Annotated  # Recommended for clearer type hinting in FastAPI
from fastapi import Depends

from application.services.client_service import ClientService
from application.services.product_service import ProductService
from application.services.worker_service import WorkerService
from application.services.form_service import FormService
from application.services.auth_service import AuthService
from application.services.update_service import UpdateService
from application.services.contacto_service import ContactoService
from application.services.chat_service import ChatService
from application.services.oferta_service import OfertaService
from application.services.leads_service import LeadsService
from infrastucture.repositories.adjuntos_repository import AdjuntosRepository
from infrastucture.external_services.gemini_provider import GeminiProvider
from application.services.brigada_service import BrigadaService
from infrastucture.repositories.client_repository import ClientRepository
from infrastucture.repositories.productos_repository import ProductRepository
from infrastucture.repositories.trabajadores_repository import WorkerRepository
from infrastucture.repositories.reportes_repository import FormRepository  # Nota el plural "repositories"
from infrastucture.repositories.brigada_repository import BrigadaRepository
from infrastucture.repositories.update_repository import UpdateRepository
from infrastucture.repositories.contacto_repository import ContactoRepository
from infrastucture.repositories.ofertas_repository import OfertasRepository
from infrastucture.repositories.leads_repository import LeadsRepository

# Global singleton instances for repositories
product_repository = ProductRepository()
worker_repository = WorkerRepository()
form_repository = FormRepository()
brigada_repository = BrigadaRepository()
client_repository = ClientRepository()
adjuntos_repository = AdjuntosRepository()
update_repository = UpdateRepository()
contacto_repository = ContactoRepository()
ofertas_repository = OfertasRepository()
leads_repository = LeadsRepository()

# Global singleton instances for external services
gemini_provider = GeminiProvider()


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
    Dependency for FastAPI that returns the singleton instance of AdjuntosRepository.
    """
    return adjuntos_repository

def get_update_repository() -> UpdateRepository:
    """
    Dependency for FastAPI that returns the singleton instance of UpdateRepository.
    """
    return update_repository

def get_contacto_repository() -> ContactoRepository:
    """
    Dependency for FastAPI that returns the singleton instance of ContactoRepository.
    """
    return contacto_repository

def get_ofertas_repository() -> OfertasRepository:
    return ofertas_repository

def get_leads_repository() -> LeadsRepository:
    """
    Dependency for FastAPI that returns the singleton instance of LeadsRepository.
    """
    return leads_repository

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

def get_contacto_service(
        contacto_repo: Annotated[ContactoRepository, Depends(get_contacto_repository)]
) -> ContactoService:
    return ContactoService(contacto_repo)



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
        client_service: Annotated[ClientService, Depends(get_client_service)],
        update_repo: Annotated[UpdateRepository, Depends(get_update_repository)]
) -> UpdateService:
    """
    Dependency for FastAPI that returns an instance of UpdateService.
    """
    return UpdateService(product_service, worker_service, client_service, update_repo)


def get_brigada_service(
        brigada_repo: Annotated[BrigadaRepository, Depends(get_brigada_repository)]
) -> BrigadaService:
    """
    Dependency for FastAPI that returns an instance of BrigadaService.
    """
    return BrigadaService(brigada_repo)


# Dependency functions for external services
def get_gemini_provider() -> GeminiProvider:
    """
    Dependency for FastAPI that returns the singleton instance of GeminiProvider.
    """
    return gemini_provider


def get_chat_service(
        gemini_prov: Annotated[GeminiProvider, Depends(get_gemini_provider)]
) -> ChatService:
    """
    Dependency for FastAPI that returns an instance of ChatService.
    """
    return ChatService(gemini_prov)




def get_oferta_service(
        ofertas_repo: Annotated[OfertasRepository, Depends(get_ofertas_repository)]
) -> OfertaService:
    return OfertaService(ofertas_repo)


def get_leads_service(
        leads_repo: Annotated[LeadsRepository, Depends(get_leads_repository)]
) -> LeadsService:
    """
    Dependency for FastAPI that returns an instance of LeadsService.
    """
    return LeadsService(leads_repo)

