# from datetime import datetime
# from typing import List, Dict, Any
# from xhtml2pdf import pisa
# from jinja2 import Template
# import io
#
#
# class BasePDFUseCase:
#     """io
#     Clase base para casos de uso de PDF que comparte funcionalidades comunes.
#     """
#
#     def _get_base_html_template(self) -> str:
#         """
#         Retorna el template HTML base que se puede extender.
#
#         Returns:
#             str: Template HTML base
#         """
#         return """
#         <!DOCTYPE html>
#         <html lang="es">
#         <head>
#             <meta charset="UTF-8">
#             <title>{{ title }} - SunCar</title>
#             <style>
#                 @page {
#                     margin: 1cm;
#                 }
#                 body {
#                     font-family: Arial, sans-serif;
#                     margin: 0;
#                     color: #333;
#                     font-size: 12px;
#                 }
#                 .header {
#                     text-align: center;
#                     border-bottom: 2px solid #2c3e50;
#                     padding-bottom: 20px;
#                     margin-bottom: 30px;
#                 }
#                 .company-name {
#                     font-size: 24px;
#                     font-weight: bold;
#                     color: #2c3e50;
#                     margin: 0;
#                 }
#                 .report-title {
#                     font-size: 18px;
#                     color: #34495e;
#                     margin: 10px 0;
#                 }
#                 .report-date {
#                     font-size: 12px;
#                     color: #7f8c8d;
#                 }
#                 .summary {
#                     background-color: #f8f9fa;
#                     padding: 15px;
#                     border-radius: 5px;
#                     margin-bottom: 20px;
#                     border: 1px solid #e9ecef;
#                 }
#                 .summary-grid {
#                     width: 100%;
#                 }
#                 .summary-item {
#                     text-align: center;
#                     display: inline-block;
#                     width: 30%;
#                     margin: 0 1.5%;
#                 }
#                 .summary-number {
#                     font-size: 18px;
#                     font-weight: bold;
#                     color: #2c3e50;
#                 }
#                 .summary-label {
#                     font-size: 10px;
#                     color: #7f8c8d;
#                 }
#                 table {
#                     width: 100%;
#                     border-collapse: collapse;
#                     margin-top: 20px;
#                 }
#                 th {
#                     background-color: #2c3e50;
#                     color: white;
#                     padding: 8px;
#                     text-align: left;
#                     font-size: 11px;
#                 }
#                 td {
#                     padding: 8px;
#                     border-bottom: 1px solid #ecf0f1;
#                     font-size: 10px;
#                 }
#                 tr:nth-child(even) {
#                     background-color: #f8f9fa;
#                 }
#                 .salary {
#                     font-weight: bold;
#                     color: #27ae60;
#                 }
#                 .footer {
#                     margin-top: 30px;
#                     text-align: center;
#                     font-size: 10px;
#                     color: #7f8c8d;
#                     border-top: 1px solid #ecf0f1;
#                     padding-top: 15px;
#                 }
#             </style>
#         </head>
#         <body>
#             <div class="header">
#                 <h1 class="company-name">SunCar</h1>
#                 <h2 class="report-title">{{ title }}</h2>
#                 <p class="report-date">Generado el: {{ fecha_generacion }}</p>
#             </div>
#
#             {{ content }}
#
#             <div class="footer">
#                 <p>Este reporte fue generado automáticamente por el sistema SunCar</p>
#                 <p>Para consultas, contacte al departamento de Recursos Humanos</p>
#             </div>
#         </body>
#         </html>
#         """
#
#     def _generate_pdf_from_html(self, html_content: str) -> bytes:
#         """
#         Genera un PDF a partir del contenido HTML.
#
#         Args:
#             html_content: Contenido HTML a convertir a PDF
#
#         Returns:
#             bytes: Contenido del PDF generado
#
#         Raises:
#             Exception: Si hay un error generando el PDF
#         """
#         result = io.BytesIO()
#         pdf = pisa.pisaDocument(io.BytesIO(html_content.encode("utf-8")), result)
#
#         if pdf.err:
#             raise Exception("Error generando PDF")
#
#         return result.getvalue()
#
#     def _get_current_datetime(self) -> str:
#         """
#         Retorna la fecha y hora actual formateada.
#
#         Returns:
#             str: Fecha y hora actual en formato dd/mm/yyyy HH:MM:SS
#         """
#         return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
#
#     def _format_currency(self, amount: float) -> str:
#         """
#         Formatea un número como moneda.
#
#         Args:
#             amount: Cantidad a formatear
#
#         Returns:
#             str: Cantidad formateada con separadores de miles
#         """
#         return f"{amount:,.0f}"