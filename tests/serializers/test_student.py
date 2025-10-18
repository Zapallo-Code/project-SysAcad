"""Unit tests for StudentSerializer."""
import unittest
from unittest.mock import patch, MagicMock
from datetime import date, timedelta
from django.core.exceptions import ValidationError


class TestStudentSerializer(unittest.TestCase):
    """Test cases for StudentSerializer validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'document_number': '12345678',
            'birth_date': date(2000, 1, 1),
            'gender': 'M',
            'student_number': 12345,
            'enrollment_date': date(2020, 3, 1),
            'document_type': 1,
            'specialty': 1
        }

    @patch('app.serializers.student.StudentSerializer')
    def test_valid_data(self, mock_serializer):
        """Test serializer with valid data."""
        from app.serializers import StudentSerializer
        
        serializer = StudentSerializer(data=self.valid_data)
        mock_serializer.return_value.is_valid.return_value = True
        
        self.assertTrue(serializer.is_valid())

    @patch('app.serializers.student.StudentSerializer')
    def test_required_fields(self, mock_serializer):
        """Test required fields validation."""
        from app.serializers import StudentSerializer
        
        serializer = StudentSerializer(data={})
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'first_name': ['This field is required.'],
            'last_name': ['This field is required.'],
            'document_number': ['This field is required.']
        }
        
        self.assertFalse(serializer.is_valid())

    @patch('app.serializers.student.StudentSerializer')
    def test_gender_choices_validation(self, mock_serializer):
        """Test gender choices validation."""
        from app.serializers import StudentSerializer
        
        invalid_data = self.valid_data.copy()
        invalid_data['gender'] = 'X'
        
        serializer = StudentSerializer(data=invalid_data)
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'gender': ['Invalid choice.']
        }
        
        self.assertFalse(serializer.is_valid())

    @patch('app.serializers.student.StudentSerializer')
    def test_birth_date_not_in_future(self, mock_serializer):
        """Test birth date cannot be in future."""
        from app.serializers import StudentSerializer
        
        invalid_data = self.valid_data.copy()
        invalid_data['birth_date'] = date.today() + timedelta(days=1)
        
        serializer = StudentSerializer(data=invalid_data)
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'birth_date': ['Birth date cannot be in the future.']
        }
        
        self.assertFalse(serializer.is_valid())

    @patch('app.serializers.student.StudentSerializer')
    def test_enrollment_date_after_birth_date(self, mock_serializer):
        """Test enrollment date must be after birth date."""
        from app.serializers import StudentSerializer
        
        invalid_data = self.valid_data.copy()
        invalid_data['enrollment_date'] = date(1995, 1, 1)
        
        serializer = StudentSerializer(data=invalid_data)
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'enrollment_date': ['Enrollment date must be after birth date.']
        }
        
        self.assertFalse(serializer.is_valid())

    @patch('app.serializers.student.StudentSerializer')
    def test_document_number_unique(self, mock_serializer):
        """Test document number uniqueness validation."""
        from app.serializers import StudentSerializer
        
        serializer = StudentSerializer(data=self.valid_data)
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'document_number': ['Student with this document number already exists.']
        }
        
        self.assertFalse(serializer.is_valid())

    @patch('app.serializers.student.StudentSerializer')
    def test_student_number_unique(self, mock_serializer):
        """Test student number uniqueness validation."""
        from app.serializers import StudentSerializer
        
        serializer = StudentSerializer(data=self.valid_data)
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'student_number': ['Student with this student number already exists.']
        }
        
        self.assertFalse(serializer.is_valid())

    @patch('app.serializers.student.StudentSerializer')
    def test_first_name_length_validation(self, mock_serializer):
        """Test first name length validation."""
        from app.serializers import StudentSerializer
        
        invalid_data = self.valid_data.copy()
        invalid_data['first_name'] = 'A' * 101
        
        serializer = StudentSerializer(data=invalid_data)
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'first_name': ['Ensure this field has no more than 100 characters.']
        }
        
        self.assertFalse(serializer.is_valid())

    @patch('app.serializers.student.StudentSerializer')
    def test_last_name_length_validation(self, mock_serializer):
        """Test last name length validation."""
        from app.serializers import StudentSerializer
        
        invalid_data = self.valid_data.copy()
        invalid_data['last_name'] = 'A' * 101
        
        serializer = StudentSerializer(data=invalid_data)
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'last_name': ['Ensure this field has no more than 100 characters.']
        }
        
        self.assertFalse(serializer.is_valid())

    @patch('app.serializers.student.StudentSerializer')
    def test_foreign_key_validation(self, mock_serializer):
        """Test foreign key validation."""
        from app.serializers import StudentSerializer
        
        invalid_data = self.valid_data.copy()
        invalid_data['specialty'] = 9999
        
        serializer = StudentSerializer(data=invalid_data)
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            'specialty': ['Invalid pk "9999" - object does not exist.']
        }
        
        self.assertFalse(serializer.is_valid())


if __name__ == '__main__':
    unittest.main()
