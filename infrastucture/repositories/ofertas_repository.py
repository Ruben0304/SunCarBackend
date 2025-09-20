from typing import List, Optional
from bson import ObjectId

from domain.entities.oferta import Oferta
from infrastucture.database.mongo_db.connection import get_collection


class OfertasRepository:
    def __init__(self):
        self.collection_name = "ofertas"

    def _to_model(self, raw: dict) -> Oferta:
        raw["id"] = str(raw.pop("_id"))

        # Ordenar elementos por categoría si existen
        if "elementos" in raw and raw["elementos"]:
            raw["elementos"] = sorted(
                raw["elementos"],
                key=lambda x: x.get("categoria", "") or ""
            )

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

        elementos_originales = oferta.get("elementos", [])

        # Ordenar elementos igual que en _to_model para mantener consistencia con el frontend
        elementos_ordenados = sorted(
            elementos_originales,
            key=lambda x: x.get("categoria", "") or ""
        )

        if elemento_index < 0 or elemento_index >= len(elementos_ordenados):
            return False

        # Obtener el elemento que se va a eliminar del array ordenado
        elemento_a_eliminar = elementos_ordenados[elemento_index]

        # Encontrar y remover el elemento del array original
        elementos_filtrados = []
        elemento_eliminado = False

        for elemento in elementos_originales:
            # Comparar por todos los campos para encontrar el elemento exacto
            if (not elemento_eliminado and
                elemento.get("categoria") == elemento_a_eliminar.get("categoria") and
                elemento.get("descripcion") == elemento_a_eliminar.get("descripcion") and
                elemento.get("cantidad") == elemento_a_eliminar.get("cantidad") and
                elemento.get("foto") == elemento_a_eliminar.get("foto")):
                elemento_eliminado = True
                continue
            elementos_filtrados.append(elemento)

        # Actualizar la oferta con la nueva lista de elementos
        result = collection.update_one(
            {"_id": ObjectId(oferta_id)},
            {"$set": {"elementos": elementos_filtrados}}
        )
        return result.modified_count > 0

    def update_elemento(self, oferta_id: str, elemento_index: int, nuevos_datos: dict) -> bool:
        collection = get_collection(self.collection_name)

        # Primero obtener la oferta para verificar que el índice es válido
        oferta = collection.find_one({"_id": ObjectId(oferta_id)})
        if not oferta or "elementos" not in oferta:
            return False

        elementos_originales = oferta.get("elementos", [])

        # Ordenar elementos igual que en _to_model para mantener consistencia con el frontend
        elementos_ordenados = sorted(
            elementos_originales,
            key=lambda x: x.get("categoria", "") or ""
        )

        if elemento_index < 0 or elemento_index >= len(elementos_ordenados):
            return False

        # Obtener el elemento que se va a actualizar del array ordenado
        elemento_a_actualizar = elementos_ordenados[elemento_index]

        # Encontrar y actualizar el elemento en el array original
        elementos_actualizados = []
        elemento_actualizado = False

        for elemento in elementos_originales:
            # Comparar por todos los campos para encontrar el elemento exacto
            if (not elemento_actualizado and
                elemento.get("categoria") == elemento_a_actualizar.get("categoria") and
                elemento.get("descripcion") == elemento_a_actualizar.get("descripcion") and
                elemento.get("cantidad") == elemento_a_actualizar.get("cantidad") and
                elemento.get("foto") == elemento_a_actualizar.get("foto")):

                # Actualizar solo los campos proporcionados
                elemento_actualizado_data = elemento.copy()
                for key, value in nuevos_datos.items():
                    if value is not None:  # Solo actualizar campos que no sean None
                        elemento_actualizado_data[key] = value

                elementos_actualizados.append(elemento_actualizado_data)
                elemento_actualizado = True
            else:
                elementos_actualizados.append(elemento)

        # Actualizar la oferta con la nueva lista de elementos
        result = collection.update_one(
            {"_id": ObjectId(oferta_id)},
            {"$set": {"elementos": elementos_actualizados}}
        )
        return result.modified_count > 0


