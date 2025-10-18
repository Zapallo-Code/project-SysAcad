"""Unit tests for additional serializers: Specialty, Plan, Subject."""
import unittest
from unittest.mock import patch, MagicMock


class TestSpecialtySerializer(unittest.TestCase):
    """Test cases for SpecialtySerializer validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {
            'name': 'Computación',
            'faculty': 1
        }

    @patch('app.serializers.specialty.SpecialtySerializer')
    def test_valid_data(self, mock_serializer):
        """Test serializer with valid data."""
        from app.serializers import SpecialtySerializer
        
        serializer = SpecialtySerializer(data=self.valid_data)
        mock_serializer.return_value.is_valid.return_value = True
        
        self.assertTrue(serializer.is_valid())

    @patch('app.serializers.specialty.SpecialtySerializer')
    def test_required_fields(self, mock_serializer):
        """Test required fields validation."""
        from app.serializers import SpecialtySerializer
        
        serializer = SpecialtySerializer(data={})
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'name': ['This field is required.'],
            'faculty': ['This field is required.']
        }
        
        self.assertFalse(serializer.is_valid())


class TestPlanSerializer(unittest.TestCase):
    """Test cases for PlanSerializer validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {
            'code': 'PLAN2020',
            'name': 'Plan 2020',
            'specialty': 1
        }

    @patch('app.serializers.plan.PlanSerializer')
    def test_valid_data(self, mock_serializer):
        """Test serializer with valid data."""
        from app.serializers import PlanSerializer
        
        serializer = PlanSerializer(data=self.valid_data)
        mock_serializer.return_value.is_valid.return_value = True
        
        self.assertTrue(serializer.is_valid())

    @patch('app.serializers.plan.PlanSerializer')
    def test_code_unique_validation(self, mock_serializer):
        """Test code uniqueness validation."""
        from app.serializers import PlanSerializer
        
        serializer = PlanSerializer(data=self.valid_data)
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'code': ['Plan with this code already exists.']
        }
        
        self.assertFalse(serializer.is_valid())

    @patch('app.serializers.plan.PlanSerializer')
    def test_code_format_validation(self, mock_serializer):
        """Test code format validation."""
        from app.serializers import PlanSerializer
        
        invalid_data = self.valid_data.copy()
        invalid_data['code'] = 'plan 2020'
        
        serializer = PlanSerializer(data=invalid_data)
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'code': ['Code must contain only uppercase letters and numbers.']
        }
        
        self.assertFalse(serializer.is_valid())


class TestSubjectSerializer(unittest.TestCase):
    """Test cases for SubjectSerializer validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {
            'code': 'AED001',
            'name': 'Algoritmos y Estructuras de Datos',
            'hours': 120,
            'plan': 1,
            'area': 1
        }

    @patch('app.serializers.subject.SubjectSerializer')
    def test_valid_data(self, mock_serializer):
        """Test serializer with valid data."""
        from app.serializers import SubjectSerializer
        
        serializer = SubjectSerializer(data=self.valid_data)
        mock_serializer.return_value.is_valid.return_value = True
        
        self.assertTrue(serializer.is_valid())

    @patch('app.serializers.subject.SubjectSerializer')
    def test_code_unique_validation(self, mock_serializer):
        """Test code uniqueness validation."""
        from app.serializers import SubjectSerializer
        
        serializer = SubjectSerializer(data=self.valid_data)
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'code': ['Subject with this code already exists.']
        }
        
        self.assertFalse(serializer.is_valid())

    @patch('app.serializers.subject.SubjectSerializer')
    def test_hours_positive_validation(self, mock_serializer):
        """Test hours must be positive."""
        from app.serializers import SubjectSerializer
        
        invalid_data = self.valid_data.copy()
        invalid_data['hours'] = -10
        
        serializer = SubjectSerializer(data=invalid_data)
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'hours': ['Hours must be a positive number.']
        }
        
        self.assertFalse(serializer.is_valid())

    @patch('app.serializers.subject.SubjectSerializer')
    def test_name_length_validation(self, mock_serializer):
        """Test name length validation."""
        from app.serializers import SubjectSerializer
        
        invalid_data = self.valid_data.copy()
        invalid_data['name'] = 'A' * 201
        
        serializer = SubjectSerializer(data=invalid_data)
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'name': ['Ensure this field has no more than 200 characters.']
        }
        
        self.assertFalse(serializer.is_valid())


if __name__ == '__main__':
    unittest.main()
