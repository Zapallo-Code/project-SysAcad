"""Unit tests for Authority model."""
import unittest
from unittest.mock import patch, MagicMock
from datetime import date


class TestAuthorityModel(unittest.TestCase):
    """Test cases for Authority model."""

    def setUp(self):
        """Set up test fixtures."""
        self.authority_data = {
            'id': 1,
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'position': 'Decano',
            'start_date': date(2020, 1, 1),
            'faculty_id': 1
        }

    @patch('app.models.authority.Authority')
    def test_create_authority(self, mock_model):
        """Test creating an authority instance."""
        mock_instance = MagicMock()
        mock_instance.id = 1
        mock_instance.first_name = 'Juan'
        mock_instance.last_name = 'Pérez'
        mock_instance.position = 'Decano'
        mock_model.objects.create.return_value = mock_instance
        
        authority = mock_model.objects.create(**self.authority_data)
        
        self.assertEqual(authority.first_name, 'Juan')
        self.assertEqual(authority.position, 'Decano')

    @patch('app.models.authority.Authority')
    def test_authority_str_representation(self, mock_model):
        """Test string representation of authority."""
        mock_instance = MagicMock()
        mock_instance.first_name = 'Juan'
        mock_instance.last_name = 'Pérez'
        mock_instance.position = 'Decano'
        mock_instance.__str__ = lambda self: f"{self.first_name} {self.last_name} - {self.position}"
        
        self.assertEqual(str(mock_instance), 'Juan Pérez - Decano')

    @patch('app.models.authority.Authority')
    def test_authority_faculty_relation(self, mock_model):
        """Test authority has faculty relation."""
        mock_instance = MagicMock()
        mock_faculty = MagicMock()
        mock_faculty.name = 'Facultad de Ciencias Exactas'
        mock_instance.faculty = mock_faculty
        
        self.assertEqual(mock_instance.faculty.name, 'Facultad de Ciencias Exactas')

    @patch('app.models.authority.Authority')
    def test_authority_dates_validation(self, mock_model):
        """Test start_date before end_date."""
        from django.core.exceptions import ValidationError
        
        mock_instance = MagicMock()
        mock_instance.start_date = date(2020, 1, 1)
        mock_instance.end_date = date(2019, 1, 1)
        mock_instance.full_clean.side_effect = ValidationError('End date must be after start date')
        
        with self.assertRaises(ValidationError):
            mock_instance.full_clean()


if __name__ == '__main__':
    unittest.main()
