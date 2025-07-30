from datetime import datetime, timezone
from typing import List, Optional
from domain.entities.update import DataUpdateRequest, DataUpdateResponse, AppUpdateRequest, AppUpdateResponse
from application.services.product_service import ProductService
from application.services.worker_service import WorkerService
from application.services.client_service import ClientService
from infrastucture.repositories.update_repository import UpdateRepository


class UpdateService:
    def __init__(
        self,
        product_service: ProductService,
        worker_service: WorkerService,
        client_service: ClientService,
        update_repository: UpdateRepository
    ):
        self.product_service = product_service
        self.worker_service = worker_service
        self.client_service = client_service
        self.update_repository = update_repository

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
        Verifica si la aplicación está actualizada consultando la BD
        """
        try:
            print(f"[DEBUG] Checking updates for platform: {request.platform}, current_version: {request.current_version}")
            
            platform_config = self.update_repository.get_app_version_config(request.platform)
            if not platform_config:
                raise ValueError(f"Plataforma no soportada: {request.platform}")
            
            print(f"[DEBUG] Platform config found: latest_version={platform_config.latest_version}, min_version={platform_config.min_version}")
            
            current_version = request.current_version
            latest_version = platform_config.latest_version
            
            print(f"[DEBUG] Comparing versions: current='{current_version}' vs latest='{latest_version}'")
            
            is_up_to_date = self._compare_versions(current_version, latest_version) >= 0
            
            print(f"[DEBUG] Is up to date: {is_up_to_date}")
            
            if is_up_to_date:
                return AppUpdateResponse(is_up_to_date=True)
            
            # Verificar si es actualización forzada
            print(f"[DEBUG] Checking force update: current='{current_version}' vs min='{platform_config.min_version}'")
            force_update = self._compare_versions(current_version, platform_config.min_version) < 0
            
            print(f"[DEBUG] Force update: {force_update}")
            
            return AppUpdateResponse(
                is_up_to_date=False,
                latest_version=latest_version,
                download_url=platform_config.download_url,
                file_size=platform_config.file_size,
                changelog=platform_config.changelog,
                force_update=force_update
            )
        except Exception as e:
            print(f"[ERROR] Exception in check_app_updates: {str(e)}")
            raise Exception(f"Error verificando actualizaciones de app: {str(e)}")

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
        try:
            # Limpiar y validar las versiones
            version1 = str(version1).strip()
            version2 = str(version2).strip()
            
            # Separar en partes y convertir a enteros, manejando errores
            v1_parts = []
            v2_parts = []
            
            for part in version1.split('.'):
                try:
                    v1_parts.append(int(part.strip()))
                except ValueError:
                    # Si no se puede convertir, usar 0
                    v1_parts.append(0)
            
            for part in version2.split('.'):
                try:
                    v2_parts.append(int(part.strip()))
                except ValueError:
                    # Si no se puede convertir, usar 0
                    v2_parts.append(0)
            
            # Normalizar a 3 partes
            while len(v1_parts) < 3:
                v1_parts.append(0)
            while len(v2_parts) < 3:
                v2_parts.append(0)
            
            # Comparar parte por parte
            for i in range(3):
                if v1_parts[i] < v2_parts[i]:
                    return -1
                elif v1_parts[i] > v2_parts[i]:
                    return 1
            
            return 0
            
        except Exception as e:
            # En caso de error, asumir que las versiones son iguales
            print(f"Error comparing versions '{version1}' and '{version2}': {str(e)}")
            return 0 