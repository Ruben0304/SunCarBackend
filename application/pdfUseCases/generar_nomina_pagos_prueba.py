from datetime import datetime
from typing import List, Dict, Any
from xhtml2pdf import pisa
from jinja2 import Template
import io


class GenerarNominaPagosPruebaUseCase:
    """
    Caso de uso para generar un PDF de nómina de pagos usando el template real de SUNCAR.
    """

    async def execute(self) -> bytes:
        """
        Ejecuta el caso de uso para generar el PDF de nómina de pagos de prueba.
        
        Returns:
            bytes: Contenido del PDF generado
        """
        # HTML template real de SUNCAR
        html_template = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Nómina de Pagos - SUNCAR</title>
            <style>
                @page {
                    size: A4;
                    margin: 1.5cm;
                }
                
                body {
                    font-family: 'Times New Roman', serif;
                    margin: 0;
                    padding: 0;
                    background: white;
                    color: #000;
                    font-size: 12px;
                    line-height: 1.4;
                }
                
                .header {
                    width: 100%;
                    border-bottom: 2px solid #000;
                    padding-bottom: 15px;
                    margin-bottom: 20px;
                }
                
                .header-content {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    width: 100%;
                }
                
                .header-left {
                    display: flex;
                    align-items: center;
                }
                
                .header-center {
                    flex: 1;
                    text-align: center;
                }
                
                .header-right {
                    display: flex;
                    align-items: center;
                    font-size: 11px;
                }
                
                .logo {
                    width: 80px;
                    height: 80px;
                    margin-right: 20px;
                    overflow: hidden;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                
                .logo img {
                    width: 80px !important;
                    height: 80px !important;
                    max-width: 80px !important;
                    max-height: 80px !important;
                }
                
                .company-info {
                    width: 100%;
                }
                
                .company-subtitle {
                    font-size: 14px;
                    color: #666;
                    margin: 2px 0 0 0;
                    font-style: italic;
                }
                
                .document-info {
                    font-size: 11px;
                }
                
                .document-title {
                    text-align: center;
                    font-size: 18px;
                    font-weight: bold;
                    color: #000;
                    margin: 15px 0;
                    text-transform: uppercase;
                }
                
                .period-info {
                    text-align: center;
                    font-size: 12px;
                    color: #000;
                    margin-bottom: 20px;
                    border: 1px solid #000;
                    padding: 8px;
                    background: #f9f9f9;
                }
                
                .payroll-table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                    font-size: 10px;
                }
                
                .payroll-table th {
                    background: #f0f0f0;
                    border: 1px solid #000;
                    padding: 8px 4px;
                    text-align: center;
                    font-weight: bold;
                    font-size: 8px;
                }
                
                .payroll-table td {
                    border: 1px solid #000;
                    padding: 6px 4px;
                    text-align: center;
                }
                
                .payroll-table tr:nth-child(even) {
                    background: #f9f9f9;
                }
                
                .employee-name {
                    text-align: left !important;
                    font-weight: bold;
                }
                
                .currency {
                    text-align: right !important;
                }
                
                .totals-section {
                    margin-top: 20px;
                    border-top: 2px solid #000;
                    padding-top: 15px;
                }
                
                .totals-table {
                    width: 100%;
                    border-collapse: collapse;
                    font-size: 11px;
                }
                
                .totals-table th {
                    background: #e0e0e0;
                    border: 1px solid #000;
                    padding: 8px;
                    text-align: center;
                    font-weight: bold;
                }
                
                .totals-table td {
                    border: 1px solid #000;
                    padding: 8px;
                    text-align: center;
                }
                
                .grand-total {
                    background: #d0d0d0 !important;
                    font-weight: bold;
                    font-size: 12px;
                }
                
                .footer {
                    margin-top: 30px;
                    padding-top: 15px;
                    border-top: 1px solid #000;
                    text-align: center;
                    color: #000;
                    font-size: 10px;
                }
                
                .signature-section {
                    display: flex;
                    justify-content: space-between;
                    margin-top: 40px;
                }
                
                .signature-box {
                    text-align: center;
                    width: 200px;
                }
                
                .signature-line {
                    border-top: 1px solid #000;
                    margin-bottom: 5px;
                    height: 40px;
                }
                
                .signature-label {
                    font-weight: bold;
                    color: #000;
                    font-size: 10px;
                }
                
                .notes-section {
                    margin-top: 20px;
                    font-size: 10px;
                    color: #666;
                }
                
                @media print {
                    body {
                        background: white;
                    }
                    
                    .no-print {
                        display: none;
                    }
                }
            </style>
        </head>
        <body>
            <div class="header">
                <div class="header-content">
                    <div class="header-left">
                        <div class="logo">
                            <img src="public/logo.JPG" alt="Logo SUNCAR">
                        </div>
                    </div>
                    
                    <div class="header-center">
                        <!-- Espacio para información central si es necesaria -->
                    </div>
                    
                    <div class="header-right">
                        <div class="document-info">
                            <strong>Código:</strong> NOM-001<br>
                            <strong>Fecha:</strong> {{ fecha_elaboracion }}<br>
                            <strong>Página:</strong> 1 de 1
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="document-title">Nómina de Pagos</div>
            
            <div class="period-info">
                <strong>PERÍODO DE PAGO:</strong> {{ periodo_pago }} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                <strong>FECHA DE ELABORACIÓN:</strong> {{ fecha_elaboracion }}
            </div>
            
            <table class="payroll-table">
                <thead>
                    <tr>
                        <th>N°</th>
                        <th>EMPLEADO</th>
                        <th>CÉDULA</th>
                        <th>CARGO</th>
                        <th>HORAS<br>TRABAJADAS</th>
                        <th>TARIFA<br>HORA</th>
                        <th>SALARIO<br>BASE</th>
                        <th>ESTÍMULOS</th>
                        <th>SALARIO<br>TOTAL</th>
                        <th>FIRMA</th>
                    </tr>
                </thead>
                <tbody>
                    {% for empleado in empleados %}
                    <tr>
                        <td>{{ empleado.numero }}</td>
                        <td class="employee-name">{{ empleado.nombre }}</td>
                        <td>{{ empleado.cedula }}</td>
                        <td>{{ empleado.cargo }}</td>
                        <td>{{ empleado.horas_trabajadas }}</td>
                        <td class="currency">$ {{ empleado.tarifa_hora }}</td>
                        <td class="currency">$ {{ empleado.salario_base }}</td>
                        <td class="currency">$ {{ empleado.estimulos }}</td>
                        <td class="currency">$ {{ empleado.salario_total }}</td>
                        <td>__________</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            
            <div class="totals-section">
                <table class="totals-table">
                    <thead>
                        <tr>
                            <th>CONCEPTO</th>
                            <th>TOTAL HORAS</th>
                            <th>TOTAL SALARIO BASE</th>
                            <th>TOTAL ESTÍMULOS</th>
                            <th>TOTAL GENERAL</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="grand-total">
                            <td><strong>TOTALES</strong></td>
                            <td><strong>{{ total_horas }}</strong></td>
                            <td><strong>$ {{ total_salario_base }}</strong></td>
                            <td><strong>$ {{ total_estimulos }}</strong></td>
                            <td><strong>$ {{ total_general }}</strong></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div class="signature-section">
                <div class="signature-box">
                    <div class="signature-line"></div>
                    <div class="signature-label">ELABORADO POR<br>Recursos Humanos</div>
                </div>
                <div class="signature-box">
                    <div class="signature-line"></div>
                    <div class="signature-label">REVISADO POR<br>Gerencia</div>
                </div>
                <div class="signature-box">
                    <div class="signature-line"></div>
                    <div class="signature-label">APROBADO POR<br>Dirección General</div>
                </div>
            </div>
            
            <div class="notes-section">
                <strong>OBSERVACIONES:</strong><br>
                _________________________________________________________________________<br>
                _________________________________________________________________________<br>
                _________________________________________________________________________
            </div>
            
            <div class="footer">
                <p><strong>SUNCAR - ENERGÍAS RENOVABLES</strong></p>
                <p>Este documento constituye el registro oficial de pagos del período indicado</p>
                <p>Para consultas dirigirse al Departamento de Recursos Humanos</p>
            </div>
        </body>
        </html>
        """

        # Datos de prueba de empleados
        empleados_prueba = [
            {
                "numero": 1,
                "nombre": "Juan Carlos Pérez Rodríguez",
                "cedula": "12345678",
                "cargo": "Mecánico Senior",
                "horas_trabajadas": 160,
                "tarifa_hora": "15,625",
                "salario_base": "2,500,000",
                "estimulos": "437,500",
                "salario_total": "2,937,500"
            },
            {
                "numero": 2,
                "nombre": "María Elena Rodríguez Silva",
                "cedula": "87654321",
                "cargo": "Electricista",
                "horas_trabajadas": 160,
                "tarifa_hora": "13,750",
                "salario_base": "2,200,000",
                "estimulos": "385,000",
                "salario_total": "2,585,000"
            },
            {
                "numero": 3,
                "nombre": "Carlos Alberto Silva López",
                "cedula": "11223344",
                "cargo": "Técnico de Diagnóstico",
                "horas_trabajadas": 160,
                "tarifa_hora": "17,500",
                "salario_base": "2,800,000",
                "estimulos": "490,000",
                "salario_total": "3,290,000"
            },
            {
                "numero": 4,
                "nombre": "Ana Patricia López Martínez",
                "cedula": "55667788",
                "cargo": "Mecánico Junior",
                "horas_trabajadas": 160,
                "tarifa_hora": "11,250",
                "salario_base": "1,800,000",
                "estimulos": "315,000",
                "salario_total": "2,115,000"
            },
            {
                "numero": 5,
                "nombre": "Roberto Daniel Martínez González",
                "cedula": "99887766",
                "cargo": "Especialista en Suspensión",
                "horas_trabajadas": 160,
                "tarifa_hora": "16,250",
                "salario_base": "2,600,000",
                "estimulos": "455,000",
                "salario_total": "3,055,000"
            },
            {
                "numero": 6,
                "nombre": "Laura Beatriz González Herrera",
                "cedula": "33445566",
                "cargo": "Técnico de Frenos",
                "horas_trabajadas": 160,
                "tarifa_hora": "14,375",
                "salario_base": "2,300,000",
                "estimulos": "402,500",
                "salario_total": "2,702,500"
            },
            {
                "numero": 7,
                "nombre": "Miguel Ángel Herrera Castro",
                "cedula": "77889900",
                "cargo": "Especialista en Motor",
                "horas_trabajadas": 160,
                "tarifa_hora": "18,125",
                "salario_base": "2,900,000",
                "estimulos": "507,500",
                "salario_total": "3,407,500"
            },
            {
                "numero": 8,
                "nombre": "Carmen Rosa Castro Mendoza",
                "cedula": "11223355",
                "cargo": "Técnico de Transmisión",
                "horas_trabajadas": 160,
                "tarifa_hora": "15,000",
                "salario_base": "2,400,000",
                "estimulos": "420,000",
                "salario_total": "2,820,000"
            },
            {
                "numero": 9,
                "nombre": "Fernando José Mendoza Ruiz",
                "cedula": "66778899",
                "cargo": "Especialista en Electricidad",
                "horas_trabajadas": 160,
                "tarifa_hora": "16,875",
                "salario_base": "2,700,000",
                "estimulos": "472,500",
                "salario_total": "3,172,500"
            },
            {
                "numero": 10,
                "nombre": "Isabel Cristina Ruiz Vargas",
                "cedula": "44556677",
                "cargo": "Técnico de Climatización",
                "horas_trabajadas": 160,
                "tarifa_hora": "14,062",
                "salario_base": "2,250,000",
                "estimulos": "393,750",
                "salario_total": "2,643,750"
            }
        ]

        # Calcular totales
        total_horas = sum(emp["horas_trabajadas"] for emp in empleados_prueba)
        total_salario_base = sum(int(emp["salario_base"].replace(",", "")) for emp in empleados_prueba)
        total_estimulos = sum(int(emp["estimulos"].replace(",", "")) for emp in empleados_prueba)
        total_general = total_salario_base + total_estimulos

        # Formatear números para mostrar
        total_salario_base_formatted = f"{total_salario_base:,}"
        total_estimulos_formatted = f"{total_estimulos:,}"
        total_general_formatted = f"{total_general:,}"

        # Fechas
        fecha_actual = datetime.now()
        fecha_elaboracion = fecha_actual.strftime("%d/%m/%Y")
        periodo_pago = f"01/{fecha_actual.strftime('%m/%Y')} - {fecha_actual.strftime('%d/%m/%Y')}"

        # Renderizar template
        template = Template(html_template)
        html_content = template.render(
            empleados=empleados_prueba,
            fecha_elaboracion=fecha_elaboracion,
            periodo_pago=periodo_pago,
            total_horas=total_horas,
            total_salario_base=total_salario_base_formatted,
            total_estimulos=total_estimulos_formatted,
            total_general=total_general_formatted
        )

        # Generar PDF usando xhtml2pdf
        result = io.BytesIO()
        pdf = pisa.pisaDocument(io.BytesIO(html_content.encode("utf-8")), result)

        if pdf.err:
            raise Exception("Error generando PDF")

        return result.getvalue()