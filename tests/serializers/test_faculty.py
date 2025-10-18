"""Unit tests for FacultySerializer."""
import unittest
from unittest.mock import patch, MagicMock


class TestFacultySerializer(unittest.TestCase):
    """Test cases for FacultySerializer validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {
            'name': 'Facultad de Ciencias Exactas',
            'university': 1
        }

    @patch('app.serializers.faculty.FacultySerializer')
    def test_valid_data(self, mock_serializer):
        """Test serializer with valid data."""
        from app.serializers import FacultySerializer
        
        serializer = FacultySerializer(data=self.valid_data)
        mock_serializer.return_value.is_valid.return_value = True
        
        self.assertTrue(serializer.is_valid())

    @patch('app.serializers.faculty.FacultySerializer')
    def test_required_fields(self, mock_serializer):
        """Test required fields validation."""
        from app.serializers import FacultySerializer
        
        serializer = FacultySerializer(data={})
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'name': ['This field is required.'],
            'university': ['This field is required.']
        }
        
        self.assertFalse(serializer.is_valid())

    @patch('app.serializers.faculty.FacultySerializer')
    def test_name_length_validation(self, mock_serializer):
        """Test name length validation."""
        from app.serializers import FacultySerializer
        
        invalid_data = self.valid_data.copy()
        invalid_data['name'] = 'A' * 201
        
        serializer = FacultySerializer(data=invalid_data)
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'name': ['Ensure this field has no more than 200 characters.']
        }
        
        self.assertFalse(serializer.is_valid())

    @patch('app.serializers.faculty.FacultySerializer')
    def test_name_whitespace_validation(self, mock_serializer):
        """Test name whitespace validation."""
        from app.serializers import FacultySerializer
        
        invalid_data = self.valid_data.copy()
        invalid_data['name'] = '   Facultad   '
        
        serializer = FacultySerializer(data=invalid_data)
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'name': ['Name cannot start or end with whitespace.']
        }
        
        self.assertFalse(serializer.is_valid())

    @patch('app.serializers.faculty.FacultySerializer')
    def test_university_foreign_key_validation(self, mock_serializer):
        """Test university foreign key validation."""
        from app.serializers import FacultySerializer
        
        invalid_data = self.valid_data.copy()
        invalid_data['university'] = 9999
        
        serializer = FacultySerializer(data=invalid_data)
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'university': ['Invalid pk "9999" - object does not exist.']
        }
        
        self.assertFalse(serializer.is_valid())

    @patch('app.serializers.faculty.FacultySerializer')
    def test_duplicate_name_validation(self, mock_serializer):
        """Test duplicate name validation."""
        from app.serializers import FacultySerializer
        
        serializer = FacultySerializer(data=self.valid_data)
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'name': ['Faculty with this name already exists in this university.']
        }
        
        self.assertFalse(serializer.is_valid())


if __name__ == '__main__':
    unittest.main()
