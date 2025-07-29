from datetime import datetime
from typing import List, Dict, Any
from xhtml2pdf import pisa
from jinja2 import Template
import io


class PDFService:

    async def generar_pdf_salarios_prueba(self) -> bytes:
        """
        Genera un PDF de prueba con salarios de trabajadores.
        """
        # HTML template como string
        html_template = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Reporte de Salarios - SunCar</title>
            <style>
                @page {
                    margin: 1cm;
                }
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    color: #333;
                    font-size: 12px;
                }
                .header {
                    text-align: center;
                    border-bottom: 2px solid #2c3e50;
                    padding-bottom: 20px;
                    margin-bottom: 30px;
                }
                .company-name {
                    font-size: 24px;
                    font-weight: bold;
                    color: #2c3e50;
                    margin: 0;
                }
                .report-title {
                    font-size: 18px;
                    color: #34495e;
                    margin: 10px 0;
                }
                .report-date {
                    font-size: 12px;
                    color: #7f8c8d;
                }
                .summary {
                    background-color: #f8f9fa;
                    padding: 15px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                    border: 1px solid #e9ecef;
                }
                .summary-grid {
                    width: 100%;
                }
                .summary-item {
                    text-align: center;
                    display: inline-block;
                    width: 30%;
                    margin: 0 1.5%;
                }
                .summary-number {
                    font-size: 18px;
                    font-weight: bold;
                    color: #2c3e50;
                }
                .summary-label {
                    font-size: 10px;
                    color: #7f8c8d;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }
                th {
                    background-color: #2c3e50;
                    color: white;
                    padding: 8px;
                    text-align: left;
                    font-size: 11px;
                }
                td {
                    padding: 8px;
                    border-bottom: 1px solid #ecf0f1;
                    font-size: 10px;
                }
                tr:nth-child(even) {
                    background-color: #f8f9fa;
                }
                .salary {
                    font-weight: bold;
                    color: #27ae60;
                }
                .footer {
                    margin-top: 30px;
                    text-align: center;
                    font-size: 10px;
                    color: #7f8c8d;
                    border-top: 1px solid #ecf0f1;
                    padding-top: 15px;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h1 class="company-name">SunCar</h1>
                <h2 class="report-title">Reporte de Salarios</h2>
                <p class="report-date">Generado el: {{ fecha_generacion }}</p>
            </div>
            
            <div class="summary">
                <div class="summary-grid">
                    <div class="summary-item">
                        <div class="summary-number">{{ total_trabajadores }}</div>
                        <div class="summary-label">Total Trabajadores</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-number">${{ total_salarios }}</div>
                        <div class="summary-label">Total Salarios</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-number">${{ promedio_salario }}</div>
                        <div class="summary-label">Promedio Salario</div>
                    </div>
                </div>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>Nombre</th>
                        <th>CI</th>
                        <th>Cargo</th>
                        <th>Brigada</th>
                        <th>Salario</th>
                    </tr>
                </thead>
                <tbody>
                    {% for trabajador in trabajadores %}
                    <tr>
                        <td>{{ trabajador.nombre }}</td>
                        <td>{{ trabajador.ci }}</td>
                        <td>{{ trabajador.cargo }}</td>
                        <td>{{ trabajador.brigada }}</td>
                        <td class="salary">${{ trabajador.salario }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            
            <div class="footer">
                <p>Este reporte fue generado automáticamente por el sistema SunCar</p>
                <p>Para consultas, contacte al departamento de Recursos Humanos</p>
            </div>
        </body>
        </html>
        """

        # Datos de prueba de trabajadores
        trabajadores_prueba = [
            {
                "nombre": "Juan Carlos Pérez",
                "ci": "12345678",
                "cargo": "Mecánico Senior",
                "brigada": "Brigada A",
                "salario": "2,500,000"
            },
            {
                "nombre": "María Elena Rodríguez",
                "ci": "87654321",
                "cargo": "Electricista",
                "brigada": "Brigada B",
                "salario": "2,200,000"
            },
            {
                "nombre": "Carlos Alberto Silva",
                "ci": "11223344",
                "cargo": "Técnico de Diagnóstico",
                "brigada": "Brigada A",
                "salario": "2,800,000"
            },
            {
                "nombre": "Ana Patricia López",
                "ci": "55667788",
                "cargo": "Mecánico Junior",
                "brigada": "Brigada C",
                "salario": "1,800,000"
            },
            {
                "nombre": "Roberto Daniel Martínez",
                "ci": "99887766",
                "cargo": "Especialista en Suspensión",
                "brigada": "Brigada B",
                "salario": "2,600,000"
            }
        ]

        # Calcular estadísticas
        total_trabajadores = len(trabajadores_prueba)
        total_salarios = sum(int(t["salario"].replace(",", "")) for t in trabajadores_prueba)
        promedio_salario = total_salarios // total_trabajadores

        # Formatear números para mostrar
        total_salarios_formatted = f"{total_salarios:,}"
        promedio_salario_formatted = f"{promedio_salario:,}"

        # Renderizar template
        template = Template(html_template)
        html_content = template.render(
            fecha_generacion=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            trabajadores=trabajadores_prueba,
            total_trabajadores=total_trabajadores,
            total_salarios=total_salarios_formatted,
            promedio_salario=promedio_salario_formatted
        )

        # Generar PDF usando xhtml2pdf
        result = io.BytesIO()
        pdf = pisa.pisaDocument(io.BytesIO(html_content.encode("utf-8")), result)

        if pdf.err:
            raise Exception("Error generando PDF")

        return result.getvalue()

    async def generar_pdf_salarios(self, trabajadores: List[Dict[str, Any]]) -> bytes:
        """
        Genera un PDF de salarios con datos reales de trabajadores.
        """
        # HTML template como string (mismo que arriba pero sin datos hardcodeados)
        html_template = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Reporte de Salarios - SunCar</title>
            <style>
                @page {
                    margin: 1cm;
                }
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    color: #333;
                    font-size: 12px;
                }
                .header {
                    text-align: center;
                    border-bottom: 2px solid #2c3e50;
                    padding-bottom: 20px;
                    margin-bottom: 30px;
                }
                .company-name {
                    font-size: 24px;
                    font-weight: bold;
                    color: #2c3e50;
                    margin: 0;
                }
                .report-title {
                    font-size: 18px;
                    color: #34495e;
                    margin: 10px 0;
                }
                .report-date {
                    font-size: 12px;
                    color: #7f8c8d;
                }
                .summary {
                    background-color: #f8f9fa;
                    padding: 15px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                    border: 1px solid #e9ecef;
                }
                .summary-grid {
                    width: 100%;
                }
                .summary-item {
                    text-align: center;
                    display: inline-block;
                    width: 30%;
                    margin: 0 1.5%;
                }
                .summary-number {
                    font-size: 18px;
                    font-weight: bold;
                    color: #2c3e50;
                }
                .summary-label {
                    font-size: 10px;
                    color: #7f8c8d;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }
                th {
                    background-color: #2c3e50;
                    color: white;
                    padding: 8px;
                    text-align: left;
                    font-size: 11px;
                }
                td {
                    padding: 8px;
                    border-bottom: 1px solid #ecf0f1;
                    font-size: 10px;
                }
                tr:nth-child(even) {
                    background-color: #f8f9fa;
                }
                .salary {
                    font-weight: bold;
                    color: #27ae60;
                }
                .footer {
                    margin-top: 30px;
                    text-align: center;
                    font-size: 10px;
                    color: #7f8c8d;
                    border-top: 1px solid #ecf0f1;
                    padding-top: 15px;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h1 class="company-name">SunCar</h1>
                <h2 class="report-title">Reporte de Salarios</h2>
                <p class="report-date">Generado el: {{ fecha_generacion }}</p>
            </div>
            
            <div class="summary">
                <div class="summary-grid">
                    <div class="summary-item">
                        <div class="summary-number">{{ total_trabajadores }}</div>
                        <div class="summary-label">Total Trabajadores</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-number">${{ total_salarios }}</div>
                        <div class="summary-label">Total Salarios</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-number">${{ promedio_salario }}</div>
                        <div class="summary-label">Promedio Salario</div>
                    </div>
                </div>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>Nombre</th>
                        <th>CI</th>
                        <th>Cargo</th>
                        <th>Brigada</th>
                        <th>Salario</th>
                    </tr>
                </thead>
                <tbody>
                    {% for trabajador in trabajadores %}
                    <tr>
                        <td>{{ trabajador.nombre }}</td>
                        <td>{{ trabajador.ci }}</td>
                        <td>{{ trabajador.cargo }}</td>
                        <td>{{ trabajador.brigada }}</td>
                        <td class="salary">${{ trabajador.salario }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            
            <div class="footer">
                <p>Este reporte fue generado automáticamente por el sistema SunCar</p>
                <p>Para consultas, contacte al departamento de Recursos Humanos</p>
            </div>
        </body>
        </html>
        """

        # Calcular estadísticas
        total_trabajadores = len(trabajadores)
        total_salarios = sum(float(t.get("salario", 0)) for t in trabajadores)
        promedio_salario = total_salarios / total_trabajadores if total_trabajadores > 0 else 0

        # Formatear números para mostrar
        total_salarios_formatted = f"{total_salarios:,.0f}"
        promedio_salario_formatted = f"{promedio_salario:,.0f}"

        # Renderizar template
        template = Template(html_template)
        html_content = template.render(
            fecha_generacion=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            trabajadores=trabajadores,
            total_trabajadores=total_trabajadores,
            total_salarios=total_salarios_formatted,
            promedio_salario=promedio_salario_formatted
        )

        # Generar PDF usando xhtml2pdf
        result = io.BytesIO()
        pdf = pisa.pisaDocument(io.BytesIO(html_content.encode("utf-8")), result)

        if pdf.err:
            raise Exception("Error generando PDF")

        return result.getvalue()