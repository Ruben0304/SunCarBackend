from typing import List, Dict, Any, Union
from infrastucture.external_services.supabase_uploader import upload_file_to_supabase

class AdjuntosRepository:
    async def procesar_adjuntos(self, adjuntos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa y sube los adjuntos a supabase, devolviendo el mismo diccionario con las URLs.
        """
        adjuntos = adjuntos.copy()  # Evitar mutar el original
        for key in ["fotos_inicio", "fotos_fin"]:
            if key in adjuntos and isinstance(adjuntos[key], list):
                urls = []
                for file_dict in adjuntos[key]:
                    url = await upload_file_to_supabase(
                        file_content=file_dict["content"],
                        original_filename=file_dict["filename"],
                        content_type=file_dict["content_type"]
                    )
                    urls.append(url)
                adjuntos[key] = urls
        # Firma cliente
        if "firma_cliente" in adjuntos and adjuntos["firma_cliente"]:
            file_dict = adjuntos["firma_cliente"]
            url = await upload_file_to_supabase(
                file_content=file_dict["content"],
                original_filename=file_dict["filename"],
                content_type=file_dict["content_type"]
            )
            adjuntos["firma_cliente"] = url
        return adjuntos 