"""Unit tests for UniversitySerializer."""
import unittest
from unittest.mock import patch, MagicMock
from rest_framework.exceptions import ValidationError


class TestUniversitySerializer(unittest.TestCase):
    """Test cases for UniversitySerializer."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {
            'name': 'Universidad Nacional de Córdoba',
            'acronym': 'UNC'
        }

    @patch('app.serializers.university.UniversitySerializer')
    def test_valid_data_serialization(self, mock_serializer_class):
        """Test serialization with valid data."""
        from app.serializers import UniversitySerializer
        
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.validated_data = self.valid_data
        mock_serializer_class.return_value = mock_serializer
        
        serializer = UniversitySerializer(data=self.valid_data)
        
        self.assertTrue(serializer.is_valid())

    def test_validate_name_whitespace_only(self):
        """Test that name with only whitespace raises ValidationError."""
        from app.serializers import UniversitySerializer
        
        serializer = UniversitySerializer()
        
        with self.assertRaises(ValidationError):
            serializer.validate_name('   ')

    def test_validate_name_empty(self):
        """Test that empty name raises ValidationError."""
        from app.serializers import UniversitySerializer
        
        serializer = UniversitySerializer()
        
        with self.assertRaises(ValidationError):
            serializer.validate_name('')

    def test_validate_name_starts_with_number(self):
        """Test that name starting with number raises ValidationError."""
        from app.serializers import UniversitySerializer
        
        serializer = UniversitySerializer()
        
        with self.assertRaises(ValidationError):
            serializer.validate_name('123 Universidad')

    def test_validate_name_valid(self):
        """Test that valid name is processed correctly."""
        from app.serializers import UniversitySerializer
        
        serializer = UniversitySerializer()
        result = serializer.validate_name('universidad nacional')
        
        self.assertEqual(result, 'Universidad Nacional')

    def test_validate_name_strips_whitespace(self):
        """Test that name whitespace is stripped."""
        from app.serializers import UniversitySerializer
        
        serializer = UniversitySerializer()
        result = serializer.validate_name('  Universidad Nacional  ')
        
        self.assertEqual(result, 'Universidad Nacional')

    def test_validate_name_title_case(self):
        """Test that name is converted to title case."""
        from app.serializers import UniversitySerializer
        
        serializer = UniversitySerializer()
        result = serializer.validate_name('UNIVERSIDAD NACIONAL')
        
        self.assertEqual(result, 'Universidad Nacional')

    def test_validate_acronym_whitespace_only(self):
        """Test that acronym with only whitespace raises ValidationError."""
        from app.serializers import UniversitySerializer
        
        serializer = UniversitySerializer()
        
        with self.assertRaises(ValidationError):
            serializer.validate_acronym('   ')

    def test_validate_acronym_empty(self):
        """Test that empty acronym raises ValidationError."""
        from app.serializers import UniversitySerializer
        
        serializer = UniversitySerializer()
        
        with self.assertRaises(ValidationError):
            serializer.validate_acronym('')

    def test_validate_acronym_with_numbers(self):
        """Test that acronym with numbers raises ValidationError."""
        from app.serializers import UniversitySerializer
        
        serializer = UniversitySerializer()
        
        with self.assertRaises(ValidationError):
            serializer.validate_acronym('UNC123')

    def test_validate_acronym_with_special_chars(self):
        """Test that acronym with special characters raises ValidationError."""
        from app.serializers import UniversitySerializer
        
        serializer = UniversitySerializer()
        
        with self.assertRaises(ValidationError):
            serializer.validate_acronym('UN-C')

    def test_validate_acronym_valid(self):
        """Test that valid acronym is processed correctly."""
        from app.serializers import UniversitySerializer
        
        serializer = UniversitySerializer()
        result = serializer.validate_acronym('unc')
        
        self.assertEqual(result, 'UNC')

    def test_validate_acronym_uppercase(self):
        """Test that acronym is converted to uppercase."""
        from app.serializers import UniversitySerializer
        
        serializer = UniversitySerializer()
        result = serializer.validate_acronym('unc')
        
        self.assertEqual(result, 'UNC')

    def test_validate_acronym_strips_whitespace(self):
        """Test that acronym whitespace is stripped."""
        from app.serializers import UniversitySerializer
        
        serializer = UniversitySerializer()
        result = serializer.validate_acronym('  UNC  ')
        
        self.assertEqual(result, 'UNC')

    def test_validate_acronym_with_spaces(self):
        """Test that acronym with spaces is accepted."""
        from app.serializers import UniversitySerializer
        
        serializer = UniversitySerializer()
        result = serializer.validate_acronym('U N C')
        
        self.assertEqual(result, 'U N C')

    def test_name_min_length_validation(self):
        """Test name minimum length validation."""
        from app.serializers import UniversitySerializer
        
        data = {'name': 'AB', 'acronym': 'AB'}
        serializer = UniversitySerializer(data=data)
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    def test_name_max_length_validation(self):
        """Test name maximum length validation."""
        from app.serializers import UniversitySerializer
        
        data = {'name': 'A' * 101, 'acronym': 'TEST'}
        serializer = UniversitySerializer(data=data)
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    def test_acronym_min_length_validation(self):
        """Test acronym minimum length validation."""
        from app.serializers import UniversitySerializer
        
        data = {'name': 'Test University', 'acronym': 'A'}
        serializer = UniversitySerializer(data=data)
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('acronym', serializer.errors)

    def test_acronym_max_length_validation(self):
        """Test acronym maximum length validation."""
        from app.serializers import UniversitySerializer
        
        data = {'name': 'Test University', 'acronym': 'A' * 11}
        serializer = UniversitySerializer(data=data)
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('acronym', serializer.errors)

    def test_name_required(self):
        """Test that name is required."""
        from app.serializers import UniversitySerializer
        
        data = {'acronym': 'TEST'}
        serializer = UniversitySerializer(data=data)
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    def test_acronym_required(self):
        """Test that acronym is required."""
        from app.serializers import UniversitySerializer
        
        data = {'name': 'Test University'}
        serializer = UniversitySerializer(data=data)
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('acronym', serializer.errors)

    def test_read_only_fields(self):
        """Test that read-only fields are properly configured."""
        from app.serializers import UniversitySerializer
        
        read_only = UniversitySerializer.Meta.read_only_fields
        
        self.assertIn('id', read_only)
        self.assertIn('created_at', read_only)
        self.assertIn('updated_at', read_only)


if __name__ == '__main__':
    unittest.main()
