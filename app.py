from flask import Flask, send_file
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import datetime

app = Flask(__name__)

# Mock para simular uma busca real
def get_service_order_by_id(order_id):
    return {
        "id": order_id,
        "customerName": "Maria Oliveira",
        "motorcycleBrand": "HONDA",
        "motorcycleModel": "CG 160",
        "motorcycleYear": "2020",
        "motorcycleColor": "VERMELHO",
        "sellerName": "Neildo Moreno",
        "mechanicName": "Fernando Santos",
        "products": [
            {
                "productName": "Pneu traseiro MT07",
                "productBrand": "PIRELLI",
                "quantity": 2,
                "unitaryPrice": 896,
                "finalPrice": 1792
            }
        ],
        "laborPrice": 10,
        "totalCost": 1802,
        "description": "updated description",
        "serviceOrderStatus": "In Progress",
        "createdAt": "2025-04-03T12:13:42.518959",
        "startedAt": "2025-04-04T11:09:25.687315",
        "updatedAt": "2025-04-04T11:05:25.671564",
        "finishedAt": "2025-04-04T11:09:20.170737",
        "canceledAt": "2025-04-04T11:09:08.049123"
    }

@app.route('/generate-pdf/<int:order_id>')
def generate_pdf(order_id):
    data = get_service_order_by_id(order_id)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=60, bottomMargin=40)
    elements = []
    styles = getSampleStyleSheet()

    # Logo (opcional)
    try:
        logo = Image("static/logo.png", width=120, height=60)
        elements.append(logo)
    except:
        pass

    # Título
    elements.append(Paragraph(f"Ordem de Serviço #{data['id']}", styles['Title']))
    elements.append(Spacer(1, 16))

    # Dados do cliente e moto
    info = f"""
        <b>Cliente:</b> {data['customerName']}<br/>
        <b>Moto:</b> {data['motorcycleBrand']} {data['motorcycleModel']} - {data['motorcycleYear']} - {data['motorcycleColor']}<br/>
        <b>Vendedor:</b> {data['sellerName']}<br/>
        <b>Mecânico:</b> {data['mechanicName']}<br/>
        <b>Status:</b> {data['serviceOrderStatus']}<br/>
        <b>Descrição:</b> {data['description']}
    """
    elements.append(Paragraph(info, styles['Normal']))
    elements.append(Spacer(1, 16))

    # Produtos
    product_table_data = [["Produto", "Marca", "Qtd", "Valor Unitário", "Valor Total"]]
    for product in data['products']:
        product_table_data.append([
            product['productName'],
            product['productBrand'],
            str(product['quantity']),
            f"R$ {product['unitaryPrice']:.2f}",
            f"R$ {product['finalPrice']:.2f}",
        ])

    product_table = Table(product_table_data, hAlign='LEFT', colWidths=[150, 100, 40, 80, 80])
    product_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (2, 1), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(product_table)
    elements.append(Spacer(1, 16))

    # Custos
    elements.append(Paragraph(f"<b>Mão de Obra:</b> R$ {data['laborPrice']:.2f}", styles['Normal']))
    elements.append(Paragraph(f"<b>Total Geral:</b> R$ {data['totalCost']:.2f}", styles['Normal']))
    elements.append(Spacer(1, 16))

    # Datas
    def format_datetime(dt_str):
        if dt_str:
            return datetime.datetime.fromisoformat(dt_str).strftime('%d/%m/%Y %H:%M')
        return "-"

    elements.append(Paragraph(f"<b>Criada em:</b> {format_datetime(data['createdAt'])}", styles['Normal']))
    elements.append(Paragraph(f"<b>Iniciada em:</b> {format_datetime(data['startedAt'])}", styles['Normal']))
    elements.append(Paragraph(f"<b>Atualizada em:</b> {format_datetime(data['updatedAt'])}", styles['Normal']))
    elements.append(Paragraph(f"<b>Finalizada em:</b> {format_datetime(data['finishedAt'])}", styles['Normal']))
    elements.append(Paragraph(f"<b>Cancelada em:</b> {format_datetime(data['canceledAt'])}", styles['Normal']))

    # Rodapé
    def add_footer(canvas, doc):
        canvas.saveState()
        footer_text = f"Relatório gerado em {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')} | MotoManager"
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.grey)
        canvas.drawString(40, 20, footer_text)
        canvas.restoreState()

    doc.build(elements, onFirstPage=add_footer, onLaterPages=add_footer)

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"ordem-servico-{order_id}.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
