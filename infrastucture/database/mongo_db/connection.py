import os
from pymongo import MongoClient
from typing import Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDatabaseVercel:
    client: Optional[MongoClient] = None
    database = None

# Instancia singleton
mongo_db = MongoDatabaseVercel()

def get_mongodb_url() -> str:
    """
    Obtener URL de MongoDB desde variables de entorno
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

def connect_to_mongo():
    """
    Crear conexión a MongoDB optimizada para Vercel con PyMongo
    """
    if mongo_db.client is not None:
        logger.info("MongoDB connection already exists")
        return mongo_db.database

    try:
        mongodb_url = get_mongodb_url()
        database_name = get_database_name()

        logger.info("Connecting to MongoDB...")

        # Configuración optimizada para serverless/Vercel
        mongo_db.client = MongoClient(
            mongodb_url,
            # Pool settings para serverless
            maxPoolSize=1,  # Una sola conexión
            minPoolSize=0,  # Sin conexiones mínimas
            maxIdleTimeMS=45000,  # 45 segundos antes de cerrar conexiones idle
            serverSelectionTimeoutMS=5000,  # 5 segundos timeout
            socketTimeoutMS=45000,  # Socket timeout
            connectTimeoutMS=10000,  # Connection timeout
            # Configuraciones adicionales
            retryWrites=True,
            w="majority"
        )

        # Seleccionar base de datos
        mongo_db.database = mongo_db.client[database_name]

        # Verificar conexión con ping
        mongo_db.client.admin.command('ping')
        logger.info(f"✅ Successfully connected to MongoDB database: {database_name}")

        return mongo_db.database

    except Exception as e:
        logger.error(f"❌ Error connecting to MongoDB: {e}")
        raise e

def close_mongo_connection():
    """
    Cerrar conexión a MongoDB
    """
    if mongo_db.client:
        mongo_db.client.close()
        mongo_db.client = None
        mongo_db.database = None
        logger.info("🔐 MongoDB connection closed")

def get_database():
    """
    Dependency para FastAPI que asegura conexión activa
    """
    if mongo_db.client is None or mongo_db.database is None:
        return connect_to_mongo()
    return mongo_db.database

def ping_database():
    """
    Verificar que la conexión esté activa
    """
    try:
        if mongo_db.client is None:
            connect_to_mongo()

        mongo_db.client.admin.command('ping')
        return True
    except Exception as e:
        logger.error(f"Database ping failed: {e}")
        return False

def get_collection(collection_name: str):
    """
    Obtener una colección de MongoDB de manera segura
    """
    database = get_database()
    return database[collection_name]

def get_mongo_client():
    """
    Obtener cliente de MongoDB
    """
    if mongo_db.client is None:
        connect_to_mongo()
    return mongo_db.client