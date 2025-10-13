from flask import Blueprint,  send_file
from app.services.alumno_service import AlumnoService

certificado_bp = Blueprint('certificado', __name__)

@certificado_bp.route('/certificado/<int:id>/pdf', methods=['GET'])
def certificado_en_pdf(id: int):
    pdf_io = AlumnoService.generar_certificado_alumno_regular(id,'pdf')

    return send_file(pdf_io, mimetype='application/pdf', as_attachment=False)

@certificado_bp.route('/certificado/<int:id>/odt', methods=['GET'])
def certificado_en_odt(id: int):
    odt_io = AlumnoService.generar_certificado_alumno_regular(id,'odt')
    
    return send_file(
        odt_io,
        mimetype='application/vnd.oasis.opendocument.text',
        as_attachment=True,
        download_name="certificado.odt"
    )

@certificado_bp.route('/certificado/<int:id>/docx', methods=['GET'])
def reporte_en_docx(id: int):
    docx_io = AlumnoService.generar_certificado_alumno_regular(id,'docx')
    
    return send_file(
        docx_io,
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        as_attachment=True,
        download_name="certificado.docx"
    )