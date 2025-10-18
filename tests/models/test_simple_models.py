"""Unit tests for Degree model."""

import unittest
from unittest.mock import patch
from django.core.exceptions import ValidationError


class TestDegreeModel(unittest.TestCase):
    """Test cases for Degree model."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {
            "name": "Ingeniería en Sistemas",
            "description": "Carrera de grado en sistemas de información",
        }

    def test_create_degree_success(self):
        """Test creating a degree with valid data."""
        from app.models import Degree

        degree = Degree(**self.valid_data)
        self.assertEqual(degree.name, "Ingeniería en Sistemas")
        self.assertEqual(
            degree.description, "Carrera de grado en sistemas de información"
        )

    def test_str_representation(self):
        """Test string representation of degree."""
        from app.models import Degree

        degree = Degree(**self.valid_data)
        self.assertIn(self.valid_data["name"], str(degree))

    def test_name_required(self):
        """Test that name is required."""
        from app.models import Degree

        degree = Degree(description="Test description")
        with self.assertRaises((ValidationError, Exception)):
            degree.full_clean()


class TestDocumentTypeModel(unittest.TestCase):
    """Test cases for DocumentType model."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {
            "name": "DNI",
            "description": "Documento Nacional de Identidad",
        }

    def test_create_document_type_success(self):
        """Test creating a document type with valid data."""
        from app.models import DocumentType

        doc_type = DocumentType(**self.valid_data)
        self.assertEqual(doc_type.name, "DNI")

    def test_str_representation(self):
        """Test string representation."""
        from app.models import DocumentType

        doc_type = DocumentType(**self.valid_data)
        self.assertIn("DNI", str(doc_type))


class TestDepartmentModel(unittest.TestCase):
    """Test cases for Department model."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {
            "name": "Departamento de Computación",
            "description": "Departamento de ciencias de la computación",
        }

    def test_create_department_success(self):
        """Test creating a department with valid data."""
        from app.models import Department

        department = Department(**self.valid_data)
        self.assertEqual(department.name, "Departamento de Computación")


class TestAreaModel(unittest.TestCase):
    """Test cases for Area model."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {
            "name": "Área de Sistemas",
            "description": "Área de sistemas de información",
        }

    def test_create_area_success(self):
        """Test creating an area with valid data."""
        from app.models import Area

        area = Area(**self.valid_data)
        self.assertEqual(area.name, "Área de Sistemas")


class TestDedicationTypeModel(unittest.TestCase):
    """Test cases for DedicationType model."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {"name": "Dedicación Exclusiva", "hours": 40}

    def test_create_dedication_type_success(self):
        """Test creating a dedication type with valid data."""
        from app.models import DedicationType

        dedication = DedicationType(**self.valid_data)
        self.assertEqual(dedication.name, "Dedicación Exclusiva")
        self.assertEqual(dedication.hours, 40)


class TestPositionCategoryModel(unittest.TestCase):
    """Test cases for PositionCategory model."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {
            "name": "Profesor Titular",
            "description": "Máxima categoría docente",
        }

    def test_create_position_category_success(self):
        """Test creating a position category with valid data."""
        from app.models import PositionCategory

        category = PositionCategory(**self.valid_data)
        self.assertEqual(category.name, "Profesor Titular")


class TestSpecialtyTypeModel(unittest.TestCase):
    """Test cases for SpecialtyType model."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {
            "name": "Orientación",
            "description": "Tipo de especialidad por orientación",
        }

    def test_create_specialty_type_success(self):
        """Test creating a specialty type with valid data."""
        from app.models import SpecialtyType

        spec_type = SpecialtyType(**self.valid_data)
        self.assertEqual(spec_type.name, "Orientación")


if __name__ == "__main__":
    unittest.main()
