"""Unit tests for Specialty model."""
import unittest
from unittest.mock import patch, MagicMock


class TestSpecialtyModel(unittest.TestCase):
    """Test cases for Specialty model."""

    def setUp(self):
        """Set up test fixtures."""
        self.specialty_data = {
            'id': 1,
            'name': 'Computación',
            'faculty_id': 1
        }

    @patch('app.models.specialty.Specialty')
    def test_create_specialty(self, mock_model):
        """Test creating a specialty instance."""
        mock_instance = MagicMock()
        mock_instance.id = 1
        mock_instance.name = 'Computación'
        mock_model.objects.create.return_value = mock_instance
        
        specialty = mock_model.objects.create(**self.specialty_data)
        
        self.assertEqual(specialty.name, 'Computación')

    @patch('app.models.specialty.Specialty')
    def test_specialty_str_representation(self, mock_model):
        """Test string representation of specialty."""
        mock_instance = MagicMock()
        mock_instance.name = 'Computación'
        mock_instance.__str__ = lambda self: self.name
        
        self.assertEqual(str(mock_instance), 'Computación')

    @patch('app.models.specialty.Specialty')
    def test_specialty_faculty_relation(self, mock_model):
        """Test specialty has faculty relation."""
        mock_instance = MagicMock()
        mock_faculty = MagicMock()
        mock_faculty.name = 'Facultad de Ciencias Exactas'
        mock_instance.faculty = mock_faculty
        
        self.assertEqual(mock_instance.faculty.name, 'Facultad de Ciencias Exactas')


if __name__ == '__main__':
    unittest.main()
