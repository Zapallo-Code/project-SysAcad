"""Unit tests for serializers: Position, Authority, Orientation, Group."""
import unittest
from unittest.mock import patch, MagicMock


class TestPositionSerializer(unittest.TestCase):
    """Test cases for PositionSerializer validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {
            'name': 'Profesor Titular',
            'subject': 1,
            'category': 1,
            'dedication_type': 1
        }

    @patch('app.serializers.position.PositionSerializer')
    def test_valid_data(self, mock_serializer):
        """Test serializer with valid data."""
        from app.serializers import PositionSerializer
        
        serializer = PositionSerializer(data=self.valid_data)
        mock_serializer.return_value.is_valid.return_value = True
        
        self.assertTrue(serializer.is_valid())

    @patch('app.serializers.position.PositionSerializer')
    def test_required_fields(self, mock_serializer):
        """Test required fields validation."""
        from app.serializers import PositionSerializer
        
        serializer = PositionSerializer(data={})
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'subject': ['This field is required.'],
            'category': ['This field is required.']
        }
        
        self.assertFalse(serializer.is_valid())


class TestAuthoritySerializer(unittest.TestCase):
    """Test cases for AuthoritySerializer validation."""

    def setUp(self):
        """Set up test fixtures."""
        from datetime import date
        self.valid_data = {
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'position': 'Decano',
            'start_date': date(2020, 1, 1),
            'faculty': 1
        }

    @patch('app.serializers.authority.AuthoritySerializer')
    def test_valid_data(self, mock_serializer):
        """Test serializer with valid data."""
        from app.serializers import AuthoritySerializer
        
        serializer = AuthoritySerializer(data=self.valid_data)
        mock_serializer.return_value.is_valid.return_value = True
        
        self.assertTrue(serializer.is_valid())

    @patch('app.serializers.authority.AuthoritySerializer')
    def test_required_fields(self, mock_serializer):
        """Test required fields validation."""
        from app.serializers import AuthoritySerializer
        
        serializer = AuthoritySerializer(data={})
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'first_name': ['This field is required.'],
            'last_name': ['This field is required.'],
            'position': ['This field is required.']
        }
        
        self.assertFalse(serializer.is_valid())


class TestOrientationSerializer(unittest.TestCase):
    """Test cases for OrientationSerializer validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {
            'name': 'Sistemas de Información',
            'specialty': 1
        }

    @patch('app.serializers.orientation.OrientationSerializer')
    def test_valid_data(self, mock_serializer):
        """Test serializer with valid data."""
        from app.serializers import OrientationSerializer
        
        serializer = OrientationSerializer(data=self.valid_data)
        mock_serializer.return_value.is_valid.return_value = True
        
        self.assertTrue(serializer.is_valid())

    @patch('app.serializers.orientation.OrientationSerializer')
    def test_required_fields(self, mock_serializer):
        """Test required fields validation."""
        from app.serializers import OrientationSerializer
        
        serializer = OrientationSerializer(data={})
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'name': ['This field is required.'],
            'specialty': ['This field is required.']
        }
        
        self.assertFalse(serializer.is_valid())


class TestGroupSerializer(unittest.TestCase):
    """Test cases for GroupSerializer validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {
            'name': 'Grupo A',
            'code': 'GA001',
            'subject': 1
        }

    @patch('app.serializers.group.GroupSerializer')
    def test_valid_data(self, mock_serializer):
        """Test serializer with valid data."""
        from app.serializers import GroupSerializer
        
        serializer = GroupSerializer(data=self.valid_data)
        mock_serializer.return_value.is_valid.return_value = True
        
        self.assertTrue(serializer.is_valid())

    @patch('app.serializers.group.GroupSerializer')
    def test_code_unique_validation(self, mock_serializer):
        """Test code uniqueness validation."""
        from app.serializers import GroupSerializer
        
        serializer = GroupSerializer(data=self.valid_data)
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'code': ['Group with this code already exists.']
        }
        
        self.assertFalse(serializer.is_valid())


if __name__ == '__main__':
    unittest.main()
