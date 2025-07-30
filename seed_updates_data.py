"""
Script para poblar la colección 'updates' con datos iniciales
Ejecutar una sola vez para configurar los datos de versiones de app
"""

import asyncio
from datetime import datetime, timezone
from infrastucture.repositories.update_repository import UpdateRepository
from domain.entities.update import AppVersionConfig


async def seed_update_data():
    """
    Pobla la colección updates con configuración inicial de versiones
    """
    try:
        update_repo = UpdateRepository()
        
        # Configuración inicial para Android
        android_config = AppVersionConfig(
            platform="android",
            latest_version="1.5.0",
            download_url="https://phlticqaakljccwvnlop.supabase.co/storage/v1/object/public/apk/suncar.apk",
            file_size=15728640,  # 15MB
            changelog="Nuevas funcionalidades y correcciones de bugs",
            force_update=False,
            min_version="1.0.0"
        )
        
        # Usar upsert para crear o actualizar
        android_id = update_repo.upsert_app_version_config(android_config)
        print(f"✅ Configuración Android creada/actualizada con ID: {android_id}")
        
        # Si quieres agregar iOS en el futuro:
        # ios_config = AppVersionConfig(
        #     platform="ios",
        #     latest_version="1.5.0",
        #     download_url="https://apps.apple.com/app/suncar/id123456789",
        #     file_size=20971520,  # 20MB
        #     changelog="Nuevas funcionalidades y correcciones de bugs",
        #     force_update=False,
        #     min_version="1.0.0"
        # )
        # ios_id = update_repo.upsert_app_version_config(ios_config)
        # print(f"✅ Configuración iOS creada/actualizada con ID: {ios_id}")
        
        # Verificar que se guardó correctamente
        retrieved_config = update_repo.get_app_version_config("android")
        if retrieved_config:
            print("✅ Verificación exitosa - Configuración recuperada:")
            print(f"   Platform: {retrieved_config.platform}")
            print(f"   Latest Version: {retrieved_config.latest_version}")
            print(f"   Download URL: {retrieved_config.download_url}")
            print(f"   File Size: {retrieved_config.file_size} bytes")
        else:
            print("❌ Error: No se pudo recuperar la configuración")
            
    except Exception as e:
        print(f"❌ Error poblando datos: {str(e)}")


if __name__ == "__main__":
    print("🚀 Iniciando población de datos de updates...")
    asyncio.run(seed_update_data())
    print("✅ Proceso completado")