"""Unit tests for FacultySerializer."""

import unittest


class TestFacultySerializer(unittest.TestCase):
    """Test cases for FacultySerializer validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {
            "name": "Facultad de Ciencias Exactas",
            "abbreviation": "FCE",
            "directory": "direccion@fce.edu.ar",
            "acronym": "FCE",
            "email": "contacto@fce.edu.ar",
            "university_id": 1,
        }

    def test_valid_data(self):
        """Test serializer with valid data."""
        from app.serializers import FacultySerializer

        serializer = FacultySerializer(data=self.valid_data)

        self.assertTrue(serializer.is_valid(), msg=f"Errors: {serializer.errors}")

    def test_required_fields(self):
        """Test required fields validation."""
        from app.serializers import FacultySerializer

        serializer = FacultySerializer(data={})

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertIn("abbreviation", serializer.errors)
        self.assertIn("university_id", serializer.errors)

    def test_name_length_validation(self):
        """Test name length validation."""
        from app.serializers import FacultySerializer

        invalid_data = self.valid_data.copy()
        invalid_data["name"] = "A" * 101

        serializer = FacultySerializer(data=invalid_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_name_starts_with_letter(self):
        """Test name must start with letter."""
        from app.serializers import FacultySerializer

        invalid_data = self.valid_data.copy()
        invalid_data["name"] = "123 Facultad"

        serializer = FacultySerializer(data=invalid_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_invalid_email(self):
        """Test invalid email validation."""
        from app.serializers import FacultySerializer

        invalid_data = self.valid_data.copy()
        invalid_data["email"] = "not-an-email"

        serializer = FacultySerializer(data=invalid_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)


if __name__ == "__main__":
    unittest.main()
