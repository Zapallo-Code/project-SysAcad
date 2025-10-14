from abc import ABC, abstractmethod
from io import BytesIO
import os
from python_odt_template import ODTTemplate
from weasyprint import HTML
from python_odt_template.jinja import get_odt_renderer
from docxtpl import DocxTemplate
import jinja2
from django.template.loader import render_to_string
from django.conf import settings


class Document(ABC):
    @staticmethod
    @abstractmethod
    def generar(folder: str, template: str, context: dict, tipo: str) -> BytesIO:
        pass


class PDFDocument(Document):

    @staticmethod
    def generar(folder: str, template: str, context: dict) -> BytesIO:
        # Adaptar para Django
        html_string = render_to_string(f'{folder}/{template}.html', context=context)

        # En Django, usar settings.STATIC_URL en lugar de url_for
        base_url = settings.STATIC_URL if hasattr(settings, 'STATIC_URL') else '/static/'
        bytes_data = HTML(string=html_string, base_url=base_url).write_pdf()
        pdf_io = BytesIO(bytes_data)
        return pdf_io


class ODTDocument(Document):
    def generar(folder: str, template: str, context: dict) -> BytesIO:
        # Adaptar para Django - usar settings.MEDIA_ROOT
        media_path = settings.MEDIA_ROOT if hasattr(settings, 'MEDIA_ROOT') else 'media'
        odt_renderer = get_odt_renderer(media_path=media_path)

        # En Django, usar settings.BASE_DIR en lugar de current_app.root_path
        path_template = os.path.join(settings.BASE_DIR, 'app', f'{folder}', f'{template}.odt')

        odt_io = BytesIO()
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.odt', delete=False) as temp_file:
            temp_path = temp_file.name

        with ODTTemplate(path_template) as template:
            odt_renderer.render(template, context=context)
            template.pack(temp_path)
            with open(temp_path, 'rb') as f:
                odt_io.write(f.read())

        os.unlink(temp_path)
        odt_io.seek(0)
        return odt_io


class DOCXDocument(Document):
    def generar(folder: str, template: str, context: dict) -> BytesIO:

        # En Django, usar settings.BASE_DIR en lugar de current_app.root_path
        path_template = os.path.join(settings.BASE_DIR, 'app', f'{folder}', f'{template}.docx')
        doc = DocxTemplate(path_template)

        docx_io = BytesIO()
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_file:
            temp_path = temp_file.name

        jinja_env = jinja2.Environment()

        doc.render(context, jinja_env)
        doc.save(temp_path)
        with open(temp_path, 'rb') as f:
            docx_io.write(f.read())

        os.unlink(temp_path)
        docx_io.seek(0)
        return docx_io


def get_document_type(tipo: str) -> Document:
    tipos = {
        'pdf': PDFDocument,
        'odt': ODTDocument,
        'docx': DOCXDocument
    }
    return tipos.get(tipo)
