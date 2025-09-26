# from fastapi import APIRouter, HTTPException
# from fastapi.responses import Response
# from pydantic import BaseModel
# from typing import List, Dict, Any
#
# from application.pdfUseCases import GenerarSalariosPruebaUseCase, GenerarSalariosRealesUseCase, GenerarNominaPagosPruebaUseCase
#
# router = APIRouter()
#
#
# class TrabajadorSalario(BaseModel):
#     nombre: str
#     ci: str
#     cargo: str
#     brigada: str
#     salario: float
#
#
# class GenerarSalariosRequest(BaseModel):
#     trabajadores: List[TrabajadorSalario]
#
#
# @router.get("/salarios-prueba")
# async def generar_pdf_salarios_prueba():
#     """
#     Endpoint para generar un PDF de prueba con salarios de trabajadores.
#     Retorna un PDF con datos de prueba predefinidos.
#     """
#     try:
#         use_case = GenerarSalariosPruebaUseCase()
#         pdf_bytes = await use_case.execute()
#
#         return Response(
#             content=pdf_bytes,
#             media_type="application/pdf",
#             headers={
#                 "Content-Disposition": "attachment; filename=salarios_prueba.pdf"
#             }
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Error al generar PDF: {str(e)}"
#         )
#
#
# @router.get("/nomina-pagos-prueba")
# async def generar_pdf_nomina_pagos_prueba():
#     """
#     Endpoint para generar un PDF de nómina de pagos usando el template real de SUNCAR.
#     Retorna un PDF con datos de prueba predefinidos en formato de nómina oficial.
#     """
#     try:
#         use_case = GenerarNominaPagosPruebaUseCase()
#         pdf_bytes = await use_case.execute()
#
#         return Response(
#             content=pdf_bytes,
#             media_type="application/pdf",
#             headers={
#                 "Content-Disposition": "attachment; filename=nomina_pagos_prueba.pdf"
#             }
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Error al generar PDF de nómina: {str(e)}"
#         )
#
#
# @router.post("/salarios")
# async def generar_pdf_salarios(request: GenerarSalariosRequest):
#     """
#     Endpoint para generar un PDF de salarios con datos reales de trabajadores.
#     Recibe una lista de trabajadores con sus salarios y genera un PDF.
#     """
#     try:
#         # Convertir los datos del request a diccionarios
#         trabajadores_data = [
#             {
#                 "nombre": t.nombre,
#                 "ci": t.ci,
#                 "cargo": t.cargo,
#                 "brigada": t.brigada,
#                 "salario": str(t.salario)
#             }
#             for t in request.trabajadores
#         ]
#
#         use_case = GenerarSalariosRealesUseCase()
#         pdf_bytes = await use_case.execute(trabajadores_data)
#
#         return Response(
#             content=pdf_bytes,
#             media_type="application/pdf",
#             headers={
#                 "Content-Disposition": "attachment; filename=salarios.pdf"
#             }
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Error al generar PDF: {str(e)}"
#         )
#
#
# @router.get("/health")
# async def health_check():
#     """
#     Endpoint de salud para verificar que el router de PDF está funcionando.
#     """
#     return {
#         "status": "ok",
#         "message": "PDF router funcionando correctamente",
#         "available_endpoints": [
#             "GET /salarios-prueba",
#             "GET /nomina-pagos-prueba",
#             "POST /salarios",
#             "GET /health"
#         ]
#     }