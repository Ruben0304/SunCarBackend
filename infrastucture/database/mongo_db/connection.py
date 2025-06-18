import os
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import asyncio
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDatabase:
    client: Optional[AsyncIOMotorClient] = None
    database = None

# Instancia singleton
mongo_db = MongoDatabase()

def get_mongodb_url() -> str:
    """
    Obtener URL de MongoDB desde variables de entorno
    Prioriza MONGODB_URL para Vercel, fallback a MONGODB_URI
    """
    mongodb_url = os.getenv("MONGODB_URL") or os.getenv("MONGODB_URI")

    if not mongodb_url:
        raise ValueError(
            "MongoDB connection string not found. "
            "Please set MONGODB_URL or MONGODB_URI environment variable."
        )

    return mongodb_url

def get_database_name() -> str:
    """
    Obtener nombre de la base de datos desde env o usar default
    """
    return os.getenv("DATABASE_NAME", "defaultdb")

async def connect_to_mongo():
    """
    Crear conexión a MongoDB optimizada para Vercel
    """
    if mongo_db.client is not None:
        logger.info("MongoDB connection already exists")
        return

    try:
        mongodb_url = get_mongodb_url()
        database_name = get_database_name()

        logger.info("Connecting to MongoDB...")

        # Configuración optimizada para serverless/Vercel
        mongo_db.client = AsyncIOMotorClient(
            mongodb_url,
            # Pool settings para serverless
            maxPoolSize=1,  # Reducido para serverless
            minPoolSize=0,  # Sin conexiones mínimas
            maxIdleTimeMS=45000,  # 45 segundos antes de cerrar conexiones idle
            serverSelectionTimeoutMS=5000,  # 5 segundos timeout
            socketTimeoutMS=45000,  # Socket timeout
            connectTimeoutMS=10000,  # Connection timeout
            # Configuraciones adicionales para estabilidad
            retryWrites=True,
            w="majority"
        )

        # Seleccionar base de datos
        mongo_db.database = mongo_db.client[database_name]

        # Verificar conexión con ping
        await mongo_db.client.admin.command('ping')
        logger.info(f"✅ Successfully connected to MongoDB database: {database_name}")

    except Exception as e:
        logger.error(f"❌ Error connecting to MongoDB: {e}")
        # En serverless, es mejor fallar rápido
        raise e

async def close_mongo_connection():
    """
    Cerrar conexión a MongoDB
    En Vercel esto se maneja automáticamente, pero es buena práctica
    """
    if mongo_db.client:
        mongo_db.client.close()
        mongo_db.client = None
        mongo_db.database = None
        logger.info("🔐 MongoDB connection closed")

async def get_database():
    """
    Dependency para FastAPI que asegura conexión activa
    """
    if mongo_db.client is None:
        await connect_to_mongo()
    return mongo_db.database

async def ping_database():
    """
    Verificar que la conexión esté activa
    Útil para health checks
    """
    try:
        if mongo_db.client is None:
            await connect_to_mongo()

        await mongo_db.client.admin.command('ping')
        return True
    except Exception as e:
        logger.error(f"Database ping failed: {e}")
        return False

# Función para obtener colección de manera segura
async def get_collection(collection_name: str):
    """
    Obtener una colección de MongoDB de manera segura
    """
    database = await get_database()
    return database[collection_name]

# Context manager para transacciones (si usas replica sets)
class MongoTransaction:
    def __init__(self):
        self.session = None

    async def __aenter__(self):
        if mongo_db.client is None:
            await connect_to_mongo()
        self.session = await mongo_db.client.start_session()
        self.session.start_transaction()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.session.abort_transaction()
        else:
            await self.session.commit_transaction()
        await self.session.end_session()

# Para casos donde necesites la instancia del cliente directamente
async def get_mongo_client():
    """
    Obtener cliente de MongoDB
    """
    if mongo_db.client is None:
        await connect_to_mongo()
    return mongo_db.client