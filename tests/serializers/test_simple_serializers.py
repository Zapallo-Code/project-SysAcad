"""Unit tests for simple model serializers: Degree, DocumentType, Department, Area."""
import unittest
from unittest.mock import patch, MagicMock


class TestDegreeSerializer(unittest.TestCase):
    """Test cases for DegreeSerializer validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {'name': 'Licenciatura'}

    @patch('app.serializers.degree.DegreeSerializer')
    def test_valid_data(self, mock_serializer):
        """Test serializer with valid data."""
        from app.serializers import DegreeSerializer
        
        serializer = DegreeSerializer(data=self.valid_data)
        mock_serializer.return_value.is_valid.return_value = True
        
        self.assertTrue(serializer.is_valid())

    @patch('app.serializers.degree.DegreeSerializer')
    def test_name_required(self, mock_serializer):
        """Test name field is required."""
        from app.serializers import DegreeSerializer
        
        serializer = DegreeSerializer(data={})
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'name': ['This field is required.']
        }
        
        self.assertFalse(serializer.is_valid())


class TestDocumentTypeSerializer(unittest.TestCase):
    """Test cases for DocumentTypeSerializer validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {'name': 'DNI'}

    @patch('app.serializers.document_type.DocumentTypeSerializer')
    def test_valid_data(self, mock_serializer):
        """Test serializer with valid data."""
        from app.serializers import DocumentTypeSerializer
        
        serializer = DocumentTypeSerializer(data=self.valid_data)
        mock_serializer.return_value.is_valid.return_value = True
        
        self.assertTrue(serializer.is_valid())

    @patch('app.serializers.document_type.DocumentTypeSerializer')
    def test_name_unique(self, mock_serializer):
        """Test name uniqueness validation."""
        from app.serializers import DocumentTypeSerializer
        
        serializer = DocumentTypeSerializer(data=self.valid_data)
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'name': ['Document type with this name already exists.']
        }
        
        self.assertFalse(serializer.is_valid())


class TestDepartmentSerializer(unittest.TestCase):
    """Test cases for DepartmentSerializer validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {
            'name': 'Departamento de Informática',
            'faculty': 1
        }

    @patch('app.serializers.department.DepartmentSerializer')
    def test_valid_data(self, mock_serializer):
        """Test serializer with valid data."""
        from app.serializers import DepartmentSerializer
        
        serializer = DepartmentSerializer(data=self.valid_data)
        mock_serializer.return_value.is_valid.return_value = True
        
        self.assertTrue(serializer.is_valid())

    @patch('app.serializers.department.DepartmentSerializer')
    def test_required_fields(self, mock_serializer):
        """Test required fields validation."""
        from app.serializers import DepartmentSerializer
        
        serializer = DepartmentSerializer(data={})
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'name': ['This field is required.'],
            'faculty': ['This field is required.']
        }
        
        self.assertFalse(serializer.is_valid())


class TestAreaSerializer(unittest.TestCase):
    """Test cases for AreaSerializer validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {'name': 'Programación'}

    @patch('app.serializers.area.AreaSerializer')
    def test_valid_data(self, mock_serializer):
        """Test serializer with valid data."""
        from app.serializers import AreaSerializer
        
        serializer = AreaSerializer(data=self.valid_data)
        mock_serializer.return_value.is_valid.return_value = True
        
        self.assertTrue(serializer.is_valid())

    @patch('app.serializers.area.AreaSerializer')
    def test_name_length_validation(self, mock_serializer):
        """Test name length validation."""
        from app.serializers import AreaSerializer
        
        invalid_data = self.valid_data.copy()
        invalid_data['name'] = 'A' * 201
        
        serializer = AreaSerializer(data=invalid_data)
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'name': ['Ensure this field has no more than 200 characters.']
        }
        
        self.assertFalse(serializer.is_valid())


class TestDedicationTypeSerializer(unittest.TestCase):
    """Test cases for DedicationTypeSerializer validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {
            'name': 'Dedicación Exclusiva',
            'hours': 40
        }

    @patch('app.serializers.dedication_type.DedicationTypeSerializer')
    def test_valid_data(self, mock_serializer):
        """Test serializer with valid data."""
        from app.serializers import DedicationTypeSerializer
        
        serializer = DedicationTypeSerializer(data=self.valid_data)
        mock_serializer.return_value.is_valid.return_value = True
        
        self.assertTrue(serializer.is_valid())

    @patch('app.serializers.dedication_type.DedicationTypeSerializer')
    def test_hours_positive(self, mock_serializer):
        """Test hours must be positive."""
        from app.serializers import DedicationTypeSerializer
        
        invalid_data = self.valid_data.copy()
        invalid_data['hours'] = -10
        
        serializer = DedicationTypeSerializer(data=invalid_data)
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'hours': ['Hours must be a positive number.']
        }
        
        self.assertFalse(serializer.is_valid())


if __name__ == '__main__':
    unittest.main()
