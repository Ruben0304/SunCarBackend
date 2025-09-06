import logging
from infrastucture.database.mongo_db.connection import get_collection
from domain.entities.contacto import Contacto
from typing import Optional, List


class ContactoRepository:
    def __init__(self):
        self.collection_name = "contactos"
        self.logger = logging.getLogger(__name__)

    def create_contacto(self, contacto: Contacto) -> Contacto:
        """
        Crear un nuevo contacto.
        """
        collection = get_collection(self.collection_name)
        contacto_dict = contacto.model_dump(exclude={'id'})
        self.logger.info(f"Creando contacto: {contacto_dict}")
        try:
            result = collection.insert_one(contacto_dict)
            contacto.id = str(result.inserted_id)
            self.logger.info(f"Contacto creado con ID: {contacto.id}")
            return contacto
        except Exception as e:
            self.logger.error(f"Error al crear contacto: {e}")
            raise

    def find_contacto_by_id(self, contacto_id: str) -> Optional[Contacto]:
        """
        Buscar un contacto por su ID.
        """
        collection = get_collection(self.collection_name)
        self.logger.info(f"Buscando contacto por ID: {contacto_id}")
        try:
            from bson import ObjectId
            contacto_doc = collection.find_one({"_id": ObjectId(contacto_id)})
            if contacto_doc:
                contacto_doc["id"] = str(contacto_doc.pop("_id"))
                self.logger.info(f"Contacto encontrado: {contacto_doc}")
                return Contacto.model_validate(contacto_doc)
            self.logger.info("Contacto no encontrado")
            return None
        except Exception as e:
            self.logger.error(f"Error al buscar contacto: {e}")
            raise

    def update_contacto(self, contacto_id: str, contacto: Contacto) -> bool:
        """
        Actualizar un contacto existente.
        """
        collection = get_collection(self.collection_name)
        self.logger.info(f"Actualizando contacto {contacto_id} con datos: {contacto}")
        try:
            from bson import ObjectId
            contacto_dict = contacto.model_dump(exclude={'id'})
            result = collection.update_one(
                {"_id": ObjectId(contacto_id)},
                {"$set": contacto_dict}
            )
            success = result.modified_count > 0
            self.logger.info(f"Contacto actualizado: {success}")
            return success
        except Exception as e:
            self.logger.error(f"Error al actualizar contacto: {e}")
            raise

    def get_all_contactos(self) -> List[Contacto]:
        """
        Obtener todos los contactos.
        """
        collection = get_collection(self.collection_name)
        self.logger.info("Obteniendo todos los contactos")
        try:
            cursor = collection.find()
            contactos = []
            for doc in cursor:
                doc["id"] = str(doc.pop("_id"))
                contactos.append(Contacto.model_validate(doc))
            self.logger.info(f"Contactos encontrados: {len(contactos)}")
            return contactos
        except Exception as e:
            self.logger.error(f"Error al obtener contactos: {e}")
            raise

    def get_first_contacto(self) -> Optional[Contacto]:
        """
        Obtener el primer contacto de la base de datos.
        """
        collection = get_collection(self.collection_name)
        self.logger.info("Obteniendo el primer contacto")
        try:
            contacto_doc = collection.find_one()
            if contacto_doc:
                contacto_doc["id"] = str(contacto_doc.pop("_id"))
                self.logger.info(f"Primer contacto encontrado: {contacto_doc}")
                return Contacto.model_validate(contacto_doc)
            self.logger.info("No se encontraron contactos")
            return None
        except Exception as e:
            self.logger.error(f"Error al obtener el primer contacto: {e}")
            raise

    def delete_contacto(self, contacto_id: str) -> bool:
        """
        Eliminar un contacto por su ID.
        """
        collection = get_collection(self.collection_name)
        self.logger.info(f"Eliminando contacto: {contacto_id}")
        try:
            from bson import ObjectId
            result = collection.delete_one({"_id": ObjectId(contacto_id)})
            success = result.deleted_count > 0
            self.logger.info(f"Contacto eliminado: {success}")
            return success
        except Exception as e:
            self.logger.error(f"Error al eliminar contacto: {e}")
            raise
