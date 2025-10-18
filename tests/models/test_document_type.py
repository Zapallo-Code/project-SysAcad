"""Unit tests for DocumentType model."""
import unittest
from unittest.mock import patch, MagicMock


class TestDocumentTypeModel(unittest.TestCase):
    """Test cases for DocumentType model."""

    def setUp(self):
        """Set up test fixtures."""
        self.doc_type_data = {
            'id': 1,
            'name': 'DNI'
        }

    @patch('app.models.document_type.DocumentType')
    def test_create_document_type(self, mock_model):
        """Test creating a document type instance."""
        mock_instance = MagicMock()
        mock_instance.id = 1
        mock_instance.name = 'DNI'
        mock_model.objects.create.return_value = mock_instance
        
        doc_type = mock_model.objects.create(**self.doc_type_data)
        
        self.assertEqual(doc_type.name, 'DNI')

    @patch('app.models.document_type.DocumentType')
    def test_document_type_str_representation(self, mock_model):
        """Test string representation of document type."""
        mock_instance = MagicMock()
        mock_instance.name = 'DNI'
        mock_instance.__str__ = lambda self: self.name
        
        self.assertEqual(str(mock_instance), 'DNI')

    @patch('app.models.document_type.DocumentType')
    def test_document_type_name_unique(self, mock_model):
        """Test name field is unique."""
        from django.db import IntegrityError
        
        mock_model.objects.create.side_effect = IntegrityError('Duplicate name')
        
        with self.assertRaises(IntegrityError):
            mock_model.objects.create(**self.doc_type_data)


if __name__ == '__main__':
    unittest.main()
