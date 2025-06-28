from typing import List, Optional
from fastapi import Depends

from domain.entities.trabajador import Trabajador
from domain.entities.brigada import Brigada
from infrastucture.repositories.trabajadores_repository import WorkerRepository
from infrastucture.repositories.brigada_repository import BrigadaRepository


class AuthService:
    def __init__(self, worker_repo: WorkerRepository, brigada_repo: BrigadaRepository):
        self.worker_repo = worker_repo
        self.brigada_repo = brigada_repo

    async def login_trabajador(self, ci: str, contraseña: str) -> Optional[Brigada]:
        """
        Autentica un trabajador usando su CI y contraseña.
        Si la autenticación es exitosa, retorna la brigada de la cual es líder.
        
        Args:
            ci: Cédula de identidad del trabajador
            contraseña: Contraseña del trabajador
            
        Returns:
            Optional[Brigada]: La brigada de la cual el trabajador es líder si las credenciales son correctas, 
                              None en caso contrario
        """
        # Primero verificar las credenciales
        is_authenticated = self.worker_repo.login(ci, contraseña)
        
        if not is_authenticated:
            return None
        
        # Si la autenticación es exitosa, buscar la brigada de la cual es líder
        try:
            brigada = self.brigada_repo.get_brigada_by_lider_ci(ci)
            return brigada
        except Exception as e:
            # Si no se encuentra la brigada, aún consideramos el login exitoso
            # pero retornamos None para la brigada
            return None
   