import requests
import os
import tempfile
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Table, TableStyle,
    Spacer, Image
)
from reportlab.lib.styles import getSampleStyleSheet

from .utils import safe_get

BASE_URL = "http://localhost:8080"
LOGIN_URL = f"{BASE_URL}/auth/login"
ORDER_URL = f"{BASE_URL}/service-orders/find-by-id"
USERNAME = "admin"
PASSWORD = "admin"


def authenticate():
    try:
        response = requests.post(LOGIN_URL, json={"username": USERNAME, "password": PASSWORD})
        print("LOGIN RESPONSE:", response.status_code, response.text)
        if response.status_code == 200:
            token = response.text.strip()
            return token
        else:
            return None
    except Exception as e:
        print("[AUTH EXCEPTION]", e)
        return None


def generate_pdf_from_service_order(order_id: int):
    token = authenticate()
    if not token:
        print("[AUTH ERROR] Failed to authenticate")
        return None

    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{ORDER_URL}/{order_id}", headers=headers)

        if response.status_code != 200:
            print("[ORDER FETCH ERROR]", response.status_code, response.text)
            return None

        data = response.json()

        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        doc = SimpleDocTemplate(tmp_file.name, pagesize=A4,
                                rightMargin=2*cm, leftMargin=2*cm,
                                topMargin=2*cm, bottomMargin=2*cm)

        styles = getSampleStyleSheet()
        story = []

        # Logo
        logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
        if os.path.exists(logo_path):
            img = Image(logo_path, width=6*cm, height=4*cm)
            story.append(img)

        # Título
        title_style = styles['Heading1']
        title_style.alignment = 1  # Centralizado
        story.append(Paragraph("Ordem de Serviço", title_style))
        story.append(Spacer(1, 1*cm))

        # Formatar a data
        created_at = safe_get(data, 'createdAt')  # Exemplo: '2025-05-05'
        formatted_date = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%f").strftime("%d/%m/%Y")
        # Informações principais
        info_data = [
            [f"Cliente: {safe_get(data, 'customerName')}", f"Data: {formatted_date}"],
            [f"Moto: {safe_get(data, 'motorcycleBrand').capitalize()} {safe_get(data, 'motorcycleModel')} {safe_get(data, 'motorcycleYear')}",
             f"Cor: {safe_get(data, 'motorcycleColor').capitalize()}"],
            [f"Vendedor: {safe_get(data, 'sellerName')}", f"Mecânico: {safe_get(data, 'mechanicName')}"]
        ]
        info_table = Table(info_data, colWidths=[9*cm, 6*cm])
        info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.5*cm))

        # Produtos + preços
        product_data = [["Descrição", "Marca", "Qtd", "V. Unitário (R$)", "V. Final (R$)"]]

        for product in data.get("products", []):
            row = [
                safe_get(product, 'productName'),
                safe_get(product, 'productBrand'),
                str(product.get('quantity') or 0),
                f"{(product.get('unitaryPrice') or 0):.2f}",
                f"{(product.get('finalPrice') or 0):.2f}"
            ]
            product_data.append(row)

        # Linha de mão de obra
        labor_price = data.get("laborPrice", 0.0)
        product_data.append(["Mão de Obra", " ", " ", " ", f"{labor_price:.2f}"])

        # Linha de total (negrito)
        total_cost = data.get("totalCost", 0.0)
        product_data.append(["TOTAL", " ", " ", " ", f"{total_cost:.2f}"])

        product_table = Table(product_data, colWidths=[6*cm, 3*cm, 1.5*cm, 3*cm, 3*cm])
        product_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Centraliza horizontalmente
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Centraliza verticalmente
            ('FONTSIZE', (0, 0), (-1, -1), 9),
        ]))

        story.append(product_table)
        story.append(Spacer(1, 0.5*cm))

        # Descrição
        story.append(Paragraph("Descrição:", styles['Heading3']))
        for line in safe_get(data, "description").splitlines():
            story.append(Paragraph(line, styles['Normal']))

        # Geração final
        doc.build(story)

        return tmp_file.name

    except Exception as e:
        print(f"[ERRO] Falha ao gerar PDF: {e}")
        return None