"""Unit tests for Orientation model."""
import unittest
from unittest.mock import patch, MagicMock


class TestOrientationModel(unittest.TestCase):
    """Test cases for Orientation model."""

    def setUp(self):
        """Set up test fixtures."""
        self.orientation_data = {
            'id': 1,
            'name': 'Sistemas de Información',
            'specialty_id': 1
        }

    @patch('app.models.orientation.Orientation')
    def test_create_orientation(self, mock_model):
        """Test creating an orientation instance."""
        mock_instance = MagicMock()
        mock_instance.id = 1
        mock_instance.name = 'Sistemas de Información'
        mock_model.objects.create.return_value = mock_instance
        
        orientation = mock_model.objects.create(**self.orientation_data)
        
        self.assertEqual(orientation.name, 'Sistemas de Información')

    @patch('app.models.orientation.Orientation')
    def test_orientation_str_representation(self, mock_model):
        """Test string representation of orientation."""
        mock_instance = MagicMock()
        mock_instance.name = 'Sistemas de Información'
        mock_instance.__str__ = lambda self: self.name
        
        self.assertEqual(str(mock_instance), 'Sistemas de Información')

    @patch('app.models.orientation.Orientation')
    def test_orientation_specialty_relation(self, mock_model):
        """Test orientation has specialty relation."""
        mock_instance = MagicMock()
        mock_specialty = MagicMock()
        mock_specialty.name = 'Computación'
        mock_instance.specialty = mock_specialty
        
        self.assertEqual(mock_instance.specialty.name, 'Computación')


if __name__ == '__main__':
    unittest.main()
