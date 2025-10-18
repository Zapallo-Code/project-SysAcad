import logging
import os
import tempfile
from abc import ABC, abstractmethod
from io import BytesIO
from typing import Dict, Optional

import jinja2
from django.conf import settings
from django.template.loader import render_to_string
from docxtpl import DocxTemplate
from python_odt_template import ODTTemplate
from python_odt_template.jinja import get_odt_renderer
from weasyprint import HTML

logger = logging.getLogger(__name__)


class Document(ABC):

    @staticmethod
    @abstractmethod
    def generate(folder: str, template: str, context: Dict) -> BytesIO:
        pass


class PDFDocument(Document):

    @staticmethod
    def generate(folder: str, template: str, context: Dict) -> BytesIO:
        logger.info(f"Generating PDF document from template: {folder}/{template}.html")

        try:
            # Render HTML template
            template_path = f"{folder}/{template}.html"
            html_string = render_to_string(template_path, context=context)

            # Generate PDF
            base_url = getattr(settings, "STATIC_URL", "/static/")
            bytes_data = HTML(string=html_string, base_url=base_url).write_pdf()

            pdf_io = BytesIO(bytes_data)
            pdf_io.seek(0)

            logger.info(f"PDF document generated successfully: {len(bytes_data)} bytes")
            return pdf_io

        except Exception as e:
            logger.error(f"Failed to generate PDF from {template_path}: {str(e)}")
            raise ValueError(f"PDF generation failed: {str(e)}") from e


class ODTDocument(Document):

    @staticmethod
    def generate(folder: str, template: str, context: Dict) -> BytesIO:
        logger.info(f"Generating ODT document from template: {folder}/{template}.odt")

        try:
            # Validate template path
            template_path = os.path.join(
                settings.BASE_DIR, "app", folder, f"{template}.odt"
            )

            if not os.path.exists(template_path):
                logger.error(f"ODT template not found: {template_path}")
                raise FileNotFoundError(f"Template not found: {template_path}")

            # Setup renderer
            media_path = getattr(settings, "MEDIA_ROOT", "media")
            odt_renderer = get_odt_renderer(media_path=media_path)

            # Generate ODT in temporary file
            odt_io = BytesIO()

            with tempfile.NamedTemporaryFile(suffix=".odt", delete=False) as temp_file:
                temp_path = temp_file.name

            try:
                with ODTTemplate(template_path) as odt_template:
                    odt_renderer.render(odt_template, context=context)
                    odt_template.pack(temp_path)

                    with open(temp_path, "rb") as f:
                        odt_io.write(f.read())

                logger.info(
                    f"ODT document generated successfully: {odt_io.tell()} bytes"
                )

            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)

            odt_io.seek(0)
            return odt_io

        except FileNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to generate ODT from {template}: {str(e)}")
            raise ValueError(f"ODT generation failed: {str(e)}") from e


class DOCXDocument(Document):

    @staticmethod
    def generate(folder: str, template: str, context: Dict) -> BytesIO:
        logger.info(f"Generating DOCX document from template: {folder}/{template}.docx")

        try:
            # Validate template path
            template_path = os.path.join(
                settings.BASE_DIR, "app", folder, f"{template}.docx"
            )

            if not os.path.exists(template_path):
                logger.error(f"DOCX template not found: {template_path}")
                raise FileNotFoundError(f"Template not found: {template_path}")

            # Load template
            doc = DocxTemplate(template_path)

            # Generate DOCX in temporary file
            docx_io = BytesIO()

            with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as temp_file:
                temp_path = temp_file.name

            try:
                # Render with Jinja2
                jinja_env = jinja2.Environment()
                doc.render(context, jinja_env)
                doc.save(temp_path)

                with open(temp_path, "rb") as f:
                    docx_io.write(f.read())

                logger.info(
                    f"DOCX document generated successfully: {docx_io.tell()} bytes"
                )

            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)

            docx_io.seek(0)
            return docx_io

        except FileNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to generate DOCX from {template}: {str(e)}")
            raise ValueError(f"DOCX generation failed: {str(e)}") from e


def get_document_generator(document_type: str) -> Optional[type[Document]]:
    generators = {"pdf": PDFDocument, "odt": ODTDocument, "docx": DOCXDocument}

    generator = generators.get(document_type.lower())

    if not generator:
        logger.warning(f"Unsupported document type: {document_type}")
        logger.info(f"Supported types: {', '.join(generators.keys())}")

    return generator
