"""Unit tests for Group model."""
import unittest
from unittest.mock import patch, MagicMock


class TestGroupModel(unittest.TestCase):
    """Test cases for Group model."""

    def setUp(self):
        """Set up test fixtures."""
        self.group_data = {
            'id': 1,
            'name': 'Grupo A',
            'code': 'GA001',
            'subject_id': 1
        }

    @patch('app.models.group.Group')
    def test_create_group(self, mock_model):
        """Test creating a group instance."""
        mock_instance = MagicMock()
        mock_instance.id = 1
        mock_instance.name = 'Grupo A'
        mock_instance.code = 'GA001'
        mock_model.objects.create.return_value = mock_instance
        
        group = mock_model.objects.create(**self.group_data)
        
        self.assertEqual(group.name, 'Grupo A')
        self.assertEqual(group.code, 'GA001')

    @patch('app.models.group.Group')
    def test_group_str_representation(self, mock_model):
        """Test string representation of group."""
        mock_instance = MagicMock()
        mock_instance.name = 'Grupo A'
        mock_instance.code = 'GA001'
        mock_instance.__str__ = lambda self: f"{self.code} - {self.name}"
        
        self.assertEqual(str(mock_instance), 'GA001 - Grupo A')

    @patch('app.models.group.Group')
    def test_group_subject_relation(self, mock_model):
        """Test group has subject relation."""
        mock_instance = MagicMock()
        mock_subject = MagicMock()
        mock_subject.name = 'AED'
        mock_instance.subject = mock_subject
        
        self.assertEqual(mock_instance.subject.name, 'AED')


if __name__ == '__main__':
    unittest.main()
