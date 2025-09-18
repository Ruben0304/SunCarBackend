from typing import List, Optional
from bson import ObjectId

from domain.entities.oferta import Oferta
from infrastucture.database.mongo_db.connection import get_collection


class OfertasRepository:
    def __init__(self):
        self.collection_name = "ofertas"

    def _to_model(self, raw: dict) -> Oferta:
        raw["id"] = str(raw.pop("_id"))
        return Oferta.model_validate(raw)

    def _to_document(self, oferta: Oferta | dict) -> dict:
        data = oferta.model_dump() if hasattr(oferta, "model_dump") else dict(oferta)
        data.pop("id", None)
        return data

    def get_all(self) -> List[Oferta]:
        collection = get_collection(self.collection_name)
        cursor = collection.find({})
        raws = cursor.to_list(length=None)
        return [self._to_model(r) for r in raws]

    def get_by_id(self, oferta_id: str) -> Optional[Oferta]:
        collection = get_collection(self.collection_name)
        raw = collection.find_one({"_id": ObjectId(oferta_id)})
        if not raw:
            return None
        return self._to_model(raw)

    def create(self, oferta: Oferta | dict) -> str:
        collection = get_collection(self.collection_name)
        doc = self._to_document(oferta)
        result = collection.insert_one(doc)
        return str(result.inserted_id)

    def update(self, oferta_id: str, new_data: dict) -> bool:
        collection = get_collection(self.collection_name)
        new_data = self._to_document(new_data)
        result = collection.update_one({"_id": ObjectId(oferta_id)}, {"$set": new_data})
        return result.modified_count > 0

    def delete(self, oferta_id: str) -> bool:
        collection = get_collection(self.collection_name)
        result = collection.delete_one({"_id": ObjectId(oferta_id)})
        return result.deleted_count > 0

    def add_elemento(self, oferta_id: str, elemento_data: dict) -> bool:
        collection = get_collection(self.collection_name)
        result = collection.update_one(
            {"_id": ObjectId(oferta_id)},
            {"$push": {"elementos": elemento_data}}
        )
        return result.modified_count > 0

    def remove_elemento(self, oferta_id: str, elemento_index: int) -> bool:
        collection = get_collection(self.collection_name)

        # Primero obtener la oferta para verificar que el índice es válido
        oferta = collection.find_one({"_id": ObjectId(oferta_id)})
        if not oferta or "elementos" not in oferta:
            return False

        elementos = oferta.get("elementos", [])
        if elemento_index < 0 or elemento_index >= len(elementos):
            return False

        # Remover el elemento por índice
        elementos.pop(elemento_index)

        # Actualizar la oferta con la nueva lista de elementos
        result = collection.update_one(
            {"_id": ObjectId(oferta_id)},
            {"$set": {"elementos": elementos}}
        )
        return result.modified_count > 0


