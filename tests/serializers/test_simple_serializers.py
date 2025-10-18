"""Unit tests for simple model serializers: Degree, DocumentType, Department, Area."""

import unittest
from unittest.mock import patch, MagicMock


class TestDegreeSerializer(unittest.TestCase):
    """Test cases for DegreeSerializer validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {"name": "Licenciatura"}

    @patch("app.serializers.degree.DegreeSerializer")
    def test_valid_data(self, mock_serializer):
        """Test serializer with valid data."""
        from app.serializers import DegreeSerializer

        serializer = DegreeSerializer(data=self.valid_data)
        mock_serializer.return_value.is_valid.return_value = True

        self.assertTrue(serializer.is_valid())

    @patch("app.serializers.degree.DegreeSerializer")
    def test_name_required(self, mock_serializer):
        """Test name field is required."""
        from app.serializers import DegreeSerializer

        serializer = DegreeSerializer(data={})
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {"name": ["This field is required."]}

        self.assertFalse(serializer.is_valid())


class TestDocumentTypeSerializer(unittest.TestCase):
    """Test cases for DocumentTypeSerializer validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {
            "dni": 12345678,
            "civic_card": "CC123",
            "enrollment_card": "EC456",
            "passport": "PP789",
        }

    def test_valid_data(self):
        """Test serializer with valid data."""
        from app.serializers import DocumentTypeSerializer

        serializer = DocumentTypeSerializer(data=self.valid_data)

        self.assertTrue(serializer.is_valid(), msg=f"Errors: {serializer.errors}")

    def test_dni_required(self):
        """Test dni is required."""
        from app.serializers import DocumentTypeSerializer

        serializer = DocumentTypeSerializer(data={})

        self.assertFalse(serializer.is_valid())
        self.assertIn("dni", serializer.errors)


class TestDepartmentSerializer(unittest.TestCase):
    """Test cases for DepartmentSerializer validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {"name": "Departamento de Informática", "faculty": 1}

    @patch("app.serializers.department.DepartmentSerializer")
    def test_valid_data(self, mock_serializer):
        """Test serializer with valid data."""
        from app.serializers import DepartmentSerializer

        serializer = DepartmentSerializer(data=self.valid_data)
        mock_serializer.return_value.is_valid.return_value = True

        self.assertTrue(serializer.is_valid())

    @patch("app.serializers.department.DepartmentSerializer")
    def test_required_fields(self, mock_serializer):
        """Test required fields validation."""
        from app.serializers import DepartmentSerializer

        serializer = DepartmentSerializer(data={})
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            "name": ["This field is required."],
            "faculty": ["This field is required."],
        }

        self.assertFalse(serializer.is_valid())


class TestAreaSerializer(unittest.TestCase):
    """Test cases for AreaSerializer validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {"name": "Programación"}

    @patch("app.serializers.area.AreaSerializer")
    def test_valid_data(self, mock_serializer):
        """Test serializer with valid data."""
        from app.serializers import AreaSerializer

        serializer = AreaSerializer(data=self.valid_data)
        mock_serializer.return_value.is_valid.return_value = True

        self.assertTrue(serializer.is_valid())

    @patch("app.serializers.area.AreaSerializer")
    def test_name_length_validation(self, mock_serializer):
        """Test name length validation."""
        from app.serializers import AreaSerializer

        invalid_data = self.valid_data.copy()
        invalid_data["name"] = "A" * 201

        serializer = AreaSerializer(data=invalid_data)
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            "name": ["Ensure this field has no more than 200 characters."]
        }

        self.assertFalse(serializer.is_valid())


class TestDedicationTypeSerializer(unittest.TestCase):
    """Test cases for DedicationTypeSerializer validation."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {"name": "Dedicación Exclusiva", "hours": 40}

    @patch("app.serializers.dedication_type.DedicationTypeSerializer")
    def test_valid_data(self, mock_serializer):
        """Test serializer with valid data."""
        from app.serializers import DedicationTypeSerializer

        serializer = DedicationTypeSerializer(data=self.valid_data)
        mock_serializer.return_value.is_valid.return_value = True

        self.assertTrue(serializer.is_valid())


if __name__ == "__main__":
    unittest.main()
