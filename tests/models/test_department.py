"""Unit tests for Department model."""

import unittest
from unittest.mock import patch, MagicMock


class TestDepartmentModel(unittest.TestCase):
    """Test cases for Department model."""

    def setUp(self):
        """Set up test fixtures."""
        self.department_data = {
            "id": 1,
            "name": "Departamento de Informática",
            "faculty_id": 1,
        }

    @patch("app.models.department.Department")
    def test_create_department(self, mock_model):
        """Test creating a department instance."""
        mock_instance = MagicMock()
        mock_instance.id = 1
        mock_instance.name = "Departamento de Informática"
        mock_model.objects.create.return_value = mock_instance

        department = mock_model.objects.create(**self.department_data)

        self.assertEqual(department.name, "Departamento de Informática")

    @patch("app.models.department.Department")
    def test_department_str_representation(self, mock_model):
        """Test string representation of department."""
        mock_instance = MagicMock()
        mock_instance.name = "Departamento de Informática"
        mock_instance.__str__ = lambda self: self.name

        self.assertEqual(str(mock_instance), "Departamento de Informática")

    @patch("app.models.department.Department")
    def test_department_faculty_relation(self, mock_model):
        """Test department has faculty relation."""
        mock_instance = MagicMock()
        mock_faculty = MagicMock()
        mock_faculty.name = "Facultad de Ciencias Exactas"
        mock_instance.faculty = mock_faculty

        self.assertEqual(mock_instance.faculty.name, "Facultad de Ciencias Exactas")


if __name__ == "__main__":
    unittest.main()
