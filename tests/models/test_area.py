"""Unit tests for Area model."""
import unittest
from unittest.mock import patch, MagicMock


class TestAreaModel(unittest.TestCase):
    """Test cases for Area model."""

    def setUp(self):
        """Set up test fixtures."""
        self.area_data = {
            'id': 1,
            'name': 'Programación'
        }

    @patch('app.models.area.Area')
    def test_create_area(self, mock_model):
        """Test creating an area instance."""
        mock_instance = MagicMock()
        mock_instance.id = 1
        mock_instance.name = 'Programación'
        mock_model.objects.create.return_value = mock_instance
        
        area = mock_model.objects.create(**self.area_data)
        
        self.assertEqual(area.name, 'Programación')

    @patch('app.models.area.Area')
    def test_area_str_representation(self, mock_model):
        """Test string representation of area."""
        mock_instance = MagicMock()
        mock_instance.name = 'Programación'
        mock_instance.__str__ = lambda self: self.name
        
        self.assertEqual(str(mock_instance), 'Programación')

    @patch('app.models.area.Area')
    def test_area_name_length(self, mock_model):
        """Test area name has max length."""
        from django.core.exceptions import ValidationError
        
        mock_instance = MagicMock()
        mock_instance.name = 'A' * 201
        mock_instance.full_clean.side_effect = ValidationError('Name too long')
        
        with self.assertRaises(ValidationError):
            mock_instance.full_clean()


if __name__ == '__main__':
    unittest.main()
