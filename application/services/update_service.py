from datetime import datetime, timezone
from typing import List, Optional
from domain.entities.update import DataUpdateRequest, DataUpdateResponse, AppUpdateRequest, AppUpdateResponse
from application.services.product_service import ProductService
from application.services.worker_service import WorkerService
from application.services.client_service import ClientService


class UpdateService:
    def __init__(
        self,
        product_service: ProductService,
        worker_service: WorkerService,
        client_service: ClientService
    ):
        self.product_service = product_service
        self.worker_service = worker_service
        self.client_service = client_service
        
        # Configuración de versiones de app (en producción esto vendría de una BD o config)
        self.app_versions = {
            "android": {
                "latest_version": "1.5.0",
                "download_url": "https://phlticqaakljccwvnlop.supabase.co/storage/v1/object/public/apk//suncar.apk",
                "file_size": 15728640,  # 15MB
                "changelog": "Nuevas funcionalidades y correcciones de bugs",
                "force_update": False,
                "min_version": "1.0.0"
            }
            
        }

    def check_data_updates(self, request: DataUpdateRequest) -> DataUpdateResponse:
        """
        Verifica si los datos están actualizados comparando timestamps
        """
        current_timestamp = datetime.now(timezone.utc)
        outdated_entities = []
        
        # Verificar cada entidad por separado
        try:
            # Verificar productos/materiales
            products_last_update = self._get_products_last_update()
            if products_last_update > request.last_update_timestamp:
                outdated_entities.append("materiales")
            
            # Verificar trabajadores
            workers_last_update = self._get_workers_last_update()
            if workers_last_update > request.last_update_timestamp:
                outdated_entities.append("trabajadores")
            
            # Verificar clientes
            clients_last_update = self._get_clients_last_update()
            if clients_last_update > request.last_update_timestamp:
                outdated_entities.append("clientes")
                
        except Exception as e:
            # Si hay error, asumir que está desactualizado
            outdated_entities = ["materiales", "trabajadores", "clientes"]
        
        is_up_to_date = len(outdated_entities) == 0
        
        return DataUpdateResponse(
            is_up_to_date=is_up_to_date,
            outdated_entities=outdated_entities,
            current_timestamp=current_timestamp
        )

    def check_app_updates(self, request: AppUpdateRequest) -> AppUpdateResponse:
        """
        Verifica si la aplicación está actualizada
        """
        platform_config = self.app_versions.get(request.platform.lower())
        if not platform_config:
            raise ValueError(f"Plataforma no soportada: {request.platform}")
        
        current_version = request.current_version
        latest_version = platform_config["latest_version"]
        
        is_up_to_date = self._compare_versions(current_version, latest_version) >= 0
        
        if is_up_to_date:
            return AppUpdateResponse(is_up_to_date=True)
        
        # Verificar si es actualización forzada
        force_update = self._compare_versions(current_version, platform_config["min_version"]) < 0
        
        return AppUpdateResponse(
            is_up_to_date=False,
            latest_version=latest_version,
            download_url=platform_config["download_url"],
            file_size=platform_config["file_size"],
            changelog=platform_config["changelog"],
            force_update=force_update
        )

    def _get_products_last_update(self) -> datetime:
        """
        Obtiene la última fecha de actualización de productos
        En una implementación real, esto consultaría la BD
        """
        # Por ahora retornamos una fecha fija, pero debería consultar la BD
        return datetime.now(timezone.utc)
    
    def _get_workers_last_update(self) -> datetime:
        """
        Obtiene la última fecha de actualización de trabajadores
        """
        return datetime.now(timezone.utc)
    
    def _get_clients_last_update(self) -> datetime:
        """
        Obtiene la última fecha de actualización de clientes
        """
        return datetime.now(timezone.utc)

    def _compare_versions(self, version1: str, version2: str) -> int:
        """
        Compara dos versiones semánticas
        Retorna: -1 si version1 < version2, 0 si igual, 1 si version1 > version2
        """
        v1_parts = [int(x) for x in version1.split('.')]
        v2_parts = [int(x) for x in version2.split('.')]
        
        # Normalizar a 3 partes
        while len(v1_parts) < 3:
            v1_parts.append(0)
        while len(v2_parts) < 3:
            v2_parts.append(0)
        
        for i in range(3):
            if v1_parts[i] < v2_parts[i]:
                return -1
            elif v1_parts[i] > v2_parts[i]:
                return 1
        
        return 0 