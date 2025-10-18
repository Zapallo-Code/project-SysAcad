"""Unit tests for StudentSerializer."""

import unittest
from datetime import date, timedelta


class TestStudentSerializer(unittest.TestCase):
    """Test cases for StudentSerializer validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {
            "first_name": "Juan",
            "last_name": "Pérez",
            "document_number": "12345678",
            "birth_date": "2000-01-01",
            "gender": "M",
            "student_number": 12345,
            "enrollment_date": "2020-03-01",
            "document_type_id": 1,
            "specialty_id": 1,
        }

    def test_valid_data(self):
        """Test serializer with valid data."""
        from app.serializers import StudentSerializer

        serializer = StudentSerializer(data=self.valid_data)

        self.assertTrue(serializer.is_valid(), msg=f"Errors: {serializer.errors}")

    def test_required_fields(self):
        """Test required fields validation."""
        from app.serializers import StudentSerializer

        serializer = StudentSerializer(data={})

        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)
        self.assertIn("last_name", serializer.errors)
        self.assertIn("document_number", serializer.errors)

    def test_gender_choices_validation(self):
        """Test gender choices validation."""
        from app.serializers import StudentSerializer

        invalid_data = self.valid_data.copy()
        invalid_data["gender"] = "X"

        serializer = StudentSerializer(data=invalid_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("gender", serializer.errors)

    def test_birth_date_not_in_future(self):
        """Test birth date cannot be in future."""
        from app.serializers import StudentSerializer

        invalid_data = self.valid_data.copy()
        future_date = (date.today() + timedelta(days=1)).isoformat()
        invalid_data["birth_date"] = future_date

        serializer = StudentSerializer(data=invalid_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("birth_date", serializer.errors)

    def test_first_name_starts_with_letter(self):
        """Test first name must start with a letter."""
        from app.serializers import StudentSerializer

        invalid_data = self.valid_data.copy()
        invalid_data["first_name"] = "123Juan"

        serializer = StudentSerializer(data=invalid_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)

    def test_student_number_positive(self):
        """Test student number must be positive."""
        from app.serializers import StudentSerializer

        invalid_data = self.valid_data.copy()
        invalid_data["student_number"] = -1

        serializer = StudentSerializer(data=invalid_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("student_number", serializer.errors)


if __name__ == "__main__":
    unittest.main()
