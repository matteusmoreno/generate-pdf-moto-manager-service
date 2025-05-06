from flask import Blueprint, request, send_file
from .pdf_generator import generate_pdf_from_service_order
import tempfile

pdf_blueprint = Blueprint('pdf', __name__)

@pdf_blueprint.route("/generate-pdf/service-order/<int:order_id>", methods=["GET"])
def generate_pdf(order_id):
    pdf_path = generate_pdf_from_service_order(order_id)

    if not pdf_path:
        return {"error": "Ordem de serviço não encontrada"}, 404

    return send_file(pdf_path, mimetype="application/pdf", as_attachment=True, download_name=f"service_order_{order_id}.pdf")
