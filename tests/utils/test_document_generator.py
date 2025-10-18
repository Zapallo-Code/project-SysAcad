"""Unit tests for document_generator utilities."""

import unittest
from unittest.mock import patch, MagicMock, mock_open
from io import BytesIO
import os


class TestPDFDocument(unittest.TestCase):
    """Test cases for PDFDocument generator."""

    def setUp(self):
        """Set up test fixtures."""
        self.folder = "templates"
        self.template = "test_document"
        self.context = {"title": "Test Document", "content": "Test content"}

    @patch("app.utils.document_generator.HTML")
    @patch("app.utils.document_generator.render_to_string")
    def test_generate_pdf_success(self, mock_render, mock_html):
        """Test generating PDF successfully."""
        from app.utils.document_generator import PDFDocument

        mock_render.return_value = "<html><body>Test</body></html>"
        mock_html_instance = MagicMock()
        mock_html_instance.write_pdf.return_value = b"PDF content"
        mock_html.return_value = mock_html_instance

        result = PDFDocument.generate(self.folder, self.template, self.context)

        self.assertIsInstance(result, BytesIO)
        mock_render.assert_called_once()
        mock_html.assert_called_once()

    @patch("app.utils.document_generator.render_to_string")
    def test_generate_pdf_template_not_found(self, mock_render):
        """Test PDF generation with non-existent template."""
        from app.utils.document_generator import PDFDocument

        mock_render.side_effect = Exception("Template not found")

        with self.assertRaises(ValueError) as context:
            PDFDocument.generate(self.folder, self.template, self.context)

        self.assertIn("PDF generation failed", str(context.exception))

    @patch("app.utils.document_generator.HTML")
    @patch("app.utils.document_generator.render_to_string")
    def test_generate_pdf_invalid_html(self, mock_render, mock_html):
        """Test PDF generation with invalid HTML."""
        from app.utils.document_generator import PDFDocument

        mock_render.return_value = "<invalid>html"
        mock_html_instance = MagicMock()
        mock_html_instance.write_pdf.side_effect = Exception("Invalid HTML")
        mock_html.return_value = mock_html_instance

        with self.assertRaises(ValueError):
            PDFDocument.generate(self.folder, self.template, self.context)


class TestODTDocument(unittest.TestCase):
    """Test cases for ODTDocument generator."""

    def setUp(self):
        """Set up test fixtures."""
        self.folder = "templates"
        self.template = "test_document"
        self.context = {"title": "Test Document", "content": "Test content"}

    @patch("app.utils.document_generator.os.path.exists")
    @patch("app.utils.document_generator.os.path.join")
    def test_generate_odt_template_not_found(self, mock_join, mock_exists):
        """Test ODT generation with non-existent template."""
        from app.utils.document_generator import ODTDocument

        mock_join.return_value = "/fake/path/template.odt"
        mock_exists.return_value = False

        with self.assertRaises(FileNotFoundError) as context:
            ODTDocument.generate(self.folder, self.template, self.context)

        self.assertIn("Template not found", str(context.exception))

    @patch("builtins.open", new_callable=mock_open, read_data=b"ODT content")
    @patch("app.utils.document_generator.os.unlink")
    @patch("app.utils.document_generator.os.path.exists")
    @patch("app.utils.document_generator.ODTTemplate")
    @patch("app.utils.document_generator.get_odt_renderer")
    @patch("app.utils.document_generator.os.path.join")
    def test_generate_odt_success(
        self,
        mock_join,
        mock_renderer,
        mock_template_class,
        mock_exists,
        mock_unlink,
        mock_file,
    ):
        """Test generating ODT successfully."""
        from app.utils.document_generator import ODTDocument

        mock_join.return_value = "/fake/path/template.odt"
        mock_exists.return_value = True

        mock_odt_template = MagicMock()
        mock_template_class.return_value.__enter__ = MagicMock(
            return_value=mock_odt_template
        )
        mock_template_class.return_value.__exit__ = MagicMock()

        mock_renderer_instance = MagicMock()
        mock_renderer.return_value = mock_renderer_instance

        result = ODTDocument.generate(self.folder, self.template, self.context)

        self.assertIsInstance(result, BytesIO)

    @patch("app.utils.document_generator.os.path.exists")
    @patch("app.utils.document_generator.os.path.join")
    @patch("app.utils.document_generator.ODTTemplate")
    @patch("app.utils.document_generator.get_odt_renderer")
    def test_generate_odt_render_error(
        self, mock_renderer, mock_template_class, mock_join, mock_exists
    ):
        """Test ODT generation with render error."""
        from app.utils.document_generator import ODTDocument

        mock_join.return_value = "/fake/path/template.odt"
        mock_exists.return_value = True

        mock_template_class.return_value.__enter__ = MagicMock(
            side_effect=Exception("Render error")
        )

        with self.assertRaises(ValueError) as context:
            ODTDocument.generate(self.folder, self.template, self.context)

        self.assertIn("ODT generation failed", str(context.exception))


class TestDOCXDocument(unittest.TestCase):
    """Test cases for DOCXDocument generator."""

    def setUp(self):
        """Set up test fixtures."""
        self.folder = "templates"
        self.template = "test_document"
        self.context = {"title": "Test Document", "content": "Test content"}

    @patch("app.utils.document_generator.os.path.exists")
    @patch("app.utils.document_generator.os.path.join")
    def test_generate_docx_template_not_found(self, mock_join, mock_exists):
        """Test DOCX generation with non-existent template."""
        from app.utils.document_generator import DOCXDocument

        mock_join.return_value = "/fake/path/template.docx"
        mock_exists.return_value = False

        with self.assertRaises(FileNotFoundError) as context:
            DOCXDocument.generate(self.folder, self.template, self.context)

        self.assertIn("Template not found", str(context.exception))

    @patch("builtins.open", new_callable=mock_open, read_data=b"DOCX content")
    @patch("app.utils.document_generator.os.unlink")
    @patch("app.utils.document_generator.os.path.exists")
    @patch("app.utils.document_generator.DocxTemplate")
    @patch("app.utils.document_generator.jinja2.Environment")
    @patch("app.utils.document_generator.os.path.join")
    def test_generate_docx_success(
        self,
        mock_join,
        mock_jinja_env,
        mock_docx_class,
        mock_exists,
        mock_unlink,
        mock_file,
    ):
        """Test generating DOCX successfully."""
        from app.utils.document_generator import DOCXDocument

        mock_join.return_value = "/fake/path/template.docx"
        mock_exists.return_value = True

        mock_doc = MagicMock()
        mock_docx_class.return_value = mock_doc

        result = DOCXDocument.generate(self.folder, self.template, self.context)

        self.assertIsInstance(result, BytesIO)
        mock_doc.render.assert_called_once()
        mock_doc.save.assert_called_once()

    @patch("app.utils.document_generator.os.path.exists")
    @patch("app.utils.document_generator.os.path.join")
    @patch("app.utils.document_generator.DocxTemplate")
    def test_generate_docx_render_error(self, mock_docx_class, mock_join, mock_exists):
        """Test DOCX generation with render error."""
        from app.utils.document_generator import DOCXDocument

        mock_join.return_value = "/fake/path/template.docx"
        mock_exists.return_value = True

        mock_doc = MagicMock()
        mock_doc.render.side_effect = Exception("Render error")
        mock_docx_class.return_value = mock_doc

        with self.assertRaises(ValueError) as context:
            DOCXDocument.generate(self.folder, self.template, self.context)

        self.assertIn("DOCX generation failed", str(context.exception))


class TestGetDocumentGenerator(unittest.TestCase):
    """Test cases for get_document_generator function."""

    def test_get_pdf_generator(self):
        """Test getting PDF generator."""
        from app.utils.document_generator import get_document_generator, PDFDocument

        generator = get_document_generator("pdf")

        self.assertEqual(generator, PDFDocument)

    def test_get_odt_generator(self):
        """Test getting ODT generator."""
        from app.utils.document_generator import get_document_generator, ODTDocument

        generator = get_document_generator("odt")

        self.assertEqual(generator, ODTDocument)

    def test_get_docx_generator(self):
        """Test getting DOCX generator."""
        from app.utils.document_generator import get_document_generator, DOCXDocument

        generator = get_document_generator("docx")

        self.assertEqual(generator, DOCXDocument)

    def test_get_generator_case_insensitive(self):
        """Test getting generator is case-insensitive."""
        from app.utils.document_generator import get_document_generator, PDFDocument

        generator = get_document_generator("PDF")

        self.assertEqual(generator, PDFDocument)

    def test_get_generator_unsupported_type(self):
        """Test getting generator with unsupported type."""
        from app.utils.document_generator import get_document_generator

        generator = get_document_generator("unsupported")

        self.assertIsNone(generator)

    def test_get_generator_empty_string(self):
        """Test getting generator with empty string."""
        from app.utils.document_generator import get_document_generator

        generator = get_document_generator("")

        self.assertIsNone(generator)


if __name__ == "__main__":
    unittest.main()
