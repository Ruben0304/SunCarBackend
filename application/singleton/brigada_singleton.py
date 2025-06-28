from typing import Optional
from domain.entities.brigada import Brigada


class BrigadaSingleton:
    """
    Singleton para almacenar la brigada del usuario autenticado.
    Esta clase mantiene una única instancia de la brigada activa en la aplicación.
    """
    _instance = None
    _brigada_activa: Optional[Brigada] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BrigadaSingleton, cls).__new__(cls)
        return cls._instance

    @classmethod
    def set_brigada_activa(cls, brigada: Brigada) -> None:
        """
        Establece la brigada activa en el singleton.
        
        Args:
            brigada: La brigada del usuario autenticado
        """
        cls._brigada_activa = brigada

    @classmethod
    def get_brigada_activa(cls) -> Optional[Brigada]:
        """
        Obtiene la brigada activa del singleton.
        
        Returns:
            Optional[Brigada]: La brigada activa o None si no hay ninguna
        """
        return cls._brigada_activa

    @classmethod
    def clear_brigada_activa(cls) -> None:
        """
        Limpia la brigada activa del singleton.
        Útil para logout o cambio de usuario.
        """
        cls._brigada_activa = None

    @classmethod
    def has_brigada_activa(cls) -> bool:
        """
        Verifica si hay una brigada activa en el singleton.
        
        Returns:
            bool: True si hay una brigada activa, False en caso contrario
        """
        return cls._brigada_activa is not None 