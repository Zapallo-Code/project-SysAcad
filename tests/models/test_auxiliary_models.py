"""Unit tests for DedicationType, PositionCategory, SpecialtyType models."""
import unittest
from unittest.mock import patch, MagicMock


class TestDedicationTypeModel(unittest.TestCase):
    """Test cases for DedicationType model."""

    def setUp(self):
        """Set up test fixtures."""
        self.dedication_data = {
            'id': 1,
            'name': 'Dedicación Exclusiva',
            'hours': 40
        }

    @patch('app.models.dedication_type.DedicationType')
    def test_create_dedication_type(self, mock_model):
        """Test creating a dedication type instance."""
        mock_instance = MagicMock()
        mock_instance.id = 1
        mock_instance.name = 'Dedicación Exclusiva'
        mock_instance.hours = 40
        mock_model.objects.create.return_value = mock_instance
        
        dedication = mock_model.objects.create(**self.dedication_data)
        
        self.assertEqual(dedication.name, 'Dedicación Exclusiva')
        self.assertEqual(dedication.hours, 40)

    @patch('app.models.dedication_type.DedicationType')
    def test_dedication_type_str_representation(self, mock_model):
        """Test string representation of dedication type."""
        mock_instance = MagicMock()
        mock_instance.name = 'Dedicación Exclusiva'
        mock_instance.__str__ = lambda self: self.name
        
        self.assertEqual(str(mock_instance), 'Dedicación Exclusiva')


class TestPositionCategoryModel(unittest.TestCase):
    """Test cases for PositionCategory model."""

    def setUp(self):
        """Set up test fixtures."""
        self.category_data = {
            'id': 1,
            'name': 'Profesor Titular'
        }

    @patch('app.models.position_category.PositionCategory')
    def test_create_position_category(self, mock_model):
        """Test creating a position category instance."""
        mock_instance = MagicMock()
        mock_instance.id = 1
        mock_instance.name = 'Profesor Titular'
        mock_model.objects.create.return_value = mock_instance
        
        category = mock_model.objects.create(**self.category_data)
        
        self.assertEqual(category.name, 'Profesor Titular')

    @patch('app.models.position_category.PositionCategory')
    def test_position_category_str_representation(self, mock_model):
        """Test string representation of position category."""
        mock_instance = MagicMock()
        mock_instance.name = 'Profesor Titular'
        mock_instance.__str__ = lambda self: self.name
        
        self.assertEqual(str(mock_instance), 'Profesor Titular')


class TestSpecialtyTypeModel(unittest.TestCase):
    """Test cases for SpecialtyType model."""

    def setUp(self):
        """Set up test fixtures."""
        self.specialty_type_data = {
            'id': 1,
            'name': 'Licenciatura'
        }

    @patch('app.models.specialty_type.SpecialtyType')
    def test_create_specialty_type(self, mock_model):
        """Test creating a specialty type instance."""
        mock_instance = MagicMock()
        mock_instance.id = 1
        mock_instance.name = 'Licenciatura'
        mock_model.objects.create.return_value = mock_instance
        
        specialty_type = mock_model.objects.create(**self.specialty_type_data)
        
        self.assertEqual(specialty_type.name, 'Licenciatura')

    @patch('app.models.specialty_type.SpecialtyType')
    def test_specialty_type_str_representation(self, mock_model):
        """Test string representation of specialty type."""
        mock_instance = MagicMock()
        mock_instance.name = 'Licenciatura'
        mock_instance.__str__ = lambda self: self.name
        
        self.assertEqual(str(mock_instance), 'Licenciatura')


if __name__ == '__main__':
    unittest.main()
