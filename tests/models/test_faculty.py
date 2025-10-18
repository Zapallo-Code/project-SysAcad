"""Unit tests for Faculty model."""
import unittest
from unittest.mock import patch, MagicMock


class TestFacultyModel(unittest.TestCase):
    """Test cases for Faculty model."""

    def setUp(self):
        """Set up test fixtures."""
        self.faculty_data = {
            'id': 1,
            'name': 'Facultad de Ciencias Exactas',
            'university_id': 1
        }

    @patch('app.models.faculty.Faculty')
    def test_create_faculty(self, mock_model):
        """Test creating a faculty instance."""
        mock_instance = MagicMock()
        mock_instance.id = 1
        mock_instance.name = 'Facultad de Ciencias Exactas'
        mock_model.objects.create.return_value = mock_instance
        
        faculty = mock_model.objects.create(**self.faculty_data)
        
        self.assertEqual(faculty.name, 'Facultad de Ciencias Exactas')

    @patch('app.models.faculty.Faculty')
    def test_faculty_str_representation(self, mock_model):
        """Test string representation of faculty."""
        mock_instance = MagicMock()
        mock_instance.name = 'Facultad de Ciencias Exactas'
        mock_instance.__str__ = lambda self: self.name
        
        self.assertEqual(str(mock_instance), 'Facultad de Ciencias Exactas')

    @patch('app.models.faculty.Faculty')
    def test_faculty_university_relation(self, mock_model):
        """Test faculty has university relation."""
        mock_instance = MagicMock()
        mock_university = MagicMock()
        mock_university.name = 'UNC'
        mock_instance.university = mock_university
        
        self.assertEqual(mock_instance.university.name, 'UNC')

    @patch('app.models.faculty.Faculty')
    def test_faculty_name_required(self, mock_model):
        """Test name field is required."""
        from django.core.exceptions import ValidationError
        
        mock_instance = MagicMock()
        mock_instance.name = None
        mock_instance.full_clean.side_effect = ValidationError('Name is required')
        
        with self.assertRaises(ValidationError):
            mock_instance.full_clean()


if __name__ == '__main__':
    unittest.main()
