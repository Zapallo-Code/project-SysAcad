from abc import ABC, abstractmethod
from io import BytesIO
import os
from flask import current_app, render_template, url_for
from python_odt_template import ODTTemplate
from weasyprint import HTML
from python_odt_template.jinja import get_odt_renderer
from docxtpl import DocxTemplate
import jinja2

class Document(ABC):
    @staticmethod
    @abstractmethod
    def generar(carpeta: str, plantilla: str, context: dict, tipo: str) -> BytesIO:
            pass
        
class PDFDocument(Document):

    @staticmethod
    def generar(carpeta: str, plantilla: str, context: dict) ->BytesIO:
        html_string = render_template(f'{carpeta}/{plantilla}.html', 
                                context=context)        
        
        base_url = url_for('static', filename='', _external=True)
        bytes_data = HTML(string=html_string, base_url=base_url).write_pdf()
        pdf_io = BytesIO(bytes_data)        
        return pdf_io

class ODTDocument(Document):
    def generar(carpeta: str, plantilla: str, context: dict) ->BytesIO:
        odt_renderer = get_odt_renderer(media_path=url_for('static', filename='media'))
        path_template = os.path.join(current_app.root_path, f'{carpeta}', f'{plantilla}.odt')
        
        odt_io = BytesIO()
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.odt', delete=False) as temp_file:
            temp_path = temp_file.name

        with ODTTemplate(path_template) as template:
            odt_renderer.render( template,
                context=context
            )
            template.pack(temp_path)
            with open(temp_path, 'rb') as f:
                odt_io.write(f.read())
            
        os.unlink(temp_path)
        odt_io.seek(0)
        return odt_io
    
class DOCXDocument(Document):
    def generar(carpeta: str, plantilla: str, context: dict) ->BytesIO:
        
        path_template = os.path.join(current_app.root_path, f'{carpeta}', f'{plantilla}.docx')
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
    
def obtener_tipo_documento(tipo:str) -> Document:
    tipos ={
        'pdf': PDFDocument,
        'odt': ODTDocument,
        'docx': DOCXDocument
    }
    return tipos.get(tipo)
