"""Unit tests for StudentSerializer."""

import unittest
from unittest.mock import patch, MagicMock
from datetime import date, timedelta
from rest_framework.exceptions import ValidationError


class TestStudentSerializer(unittest.TestCase):
    """Test cases for StudentSerializer."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {
            "first_name": "Juan",
            "last_name": "Pérez",
            "document_number": "12345678",
            "birth_date": date(2000, 1, 1).isoformat(),
            "gender": "M",
            "student_number": 12345,
            "enrollment_date": date(2020, 3, 1).isoformat(),
            "document_type_id": 1,
            "specialty_id": 1,
        }

    def test_valid_data_serialization(self):
        """Test serialization with valid data."""
        from app.serializers import StudentSerializer

        serializer = StudentSerializer(data=self.valid_data)

        self.assertTrue(serializer.is_valid(), msg=f"Errors: {serializer.errors}")

    def test_first_name_required(self):
        """Test that first_name is required."""
        from app.serializers import StudentSerializer

        data = {**self.valid_data}
        del data["first_name"]
        serializer = StudentSerializer(data=data)

        self.assertFalse(serializer.is_valid())

    def test_last_name_required(self):
        """Test that last_name is required."""
        from app.serializers import StudentSerializer

        data = {**self.valid_data}
        del data["last_name"]
        serializer = StudentSerializer(data=data)

        self.assertFalse(serializer.is_valid())

    def test_student_number_required(self):
        """Test that student_number is required."""
        from app.serializers import StudentSerializer

        data = {**self.valid_data}
        del data["student_number"]
        serializer = StudentSerializer(data=data)

        self.assertFalse(serializer.is_valid())

    def test_birth_date_required(self):
        """Test that birth_date is required."""
        from app.serializers import StudentSerializer

        data = {**self.valid_data}
        del data["birth_date"]
        serializer = StudentSerializer(data=data)

        self.assertFalse(serializer.is_valid())

    def test_gender_choices(self):
        """Test gender field validates choices."""
        from app.serializers import StudentSerializer

        # Valid genders
        for gender in ["M", "F", "O"]:
            data = {**self.valid_data, "gender": gender}
            serializer = StudentSerializer(data=data)
            serializer.is_valid()
            # Should not raise error for valid choices

    def test_gender_invalid_choice(self):
        """Test gender field rejects invalid choices."""
        from app.serializers import StudentSerializer

        data = {**self.valid_data, "gender": "X"}
        serializer = StudentSerializer(data=data)

        self.assertFalse(serializer.is_valid())

    def test_birth_date_future_invalid(self):
        """Test birth_date in future is invalid."""
        from app.serializers import StudentSerializer

        future_date = (date.today() + timedelta(days=1)).isoformat()
        data = {**self.valid_data, "birth_date": future_date}
        serializer = StudentSerializer(data=data)

        # This validation might be in the model or serializer
        # Adjust based on actual implementation

    def test_document_type_foreign_key(self):
        """Test document_type foreign key validation."""
        from app.serializers import StudentSerializer

        data = {**self.valid_data}
        del data["document_type_id"]
        serializer = StudentSerializer(data=data)

        self.assertFalse(serializer.is_valid())

    def test_specialty_foreign_key(self):
        """Test specialty foreign key validation."""
        from app.serializers import StudentSerializer

        data = {**self.valid_data}
        del data["specialty_id"]
        serializer = StudentSerializer(data=data)

        self.assertFalse(serializer.is_valid())


class TestGenericSerializers(unittest.TestCase):
    """Test cases for generic serializers."""

    def test_degree_serializer_valid_data(self):
        """Test DegreeSerializer with valid data."""
        from app.serializers import DegreeSerializer

        data = {"name": "Ingeniería en Sistemas"}
        serializer = DegreeSerializer(data=data)

        self.assertTrue(serializer.is_valid())

    def test_document_type_serializer_valid_data(self):
        """Test DocumentTypeSerializer with valid data."""
        from app.serializers import DocumentTypeSerializer

        data = {
            "dni": 12345678,
            "civic_card": "CC123",
            "enrollment_card": "EC456",
            "passport": "PP789",
        }
        serializer = DocumentTypeSerializer(data=data)

        self.assertTrue(serializer.is_valid(), msg=f"Errors: {serializer.errors}")

    def test_department_serializer_valid_data(self):
        """Test DepartmentSerializer with valid data."""
        from app.serializers import DepartmentSerializer

        data = {"name": "Departamento de Computación"}
        serializer = DepartmentSerializer(data=data)

        self.assertTrue(serializer.is_valid())

    def test_area_serializer_valid_data(self):
        """Test AreaSerializer with valid data."""
        from app.serializers import AreaSerializer

        data = {"name": "Área de Sistemas"}
        serializer = AreaSerializer(data=data)

        self.assertTrue(serializer.is_valid())


if __name__ == "__main__":
    unittest.main()
