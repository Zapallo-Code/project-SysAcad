"""Generic unit tests for simple repositories."""

import unittest
from unittest.mock import patch, MagicMock
from django.core.exceptions import ObjectDoesNotExist


class GenericRepositoryTestMixin:
    """Mixin for generic repository tests."""

    repository_class = None
    model_class = None
    valid_data = None

    def test_create_success(self):
        """Test creating an entity successfully."""
        with patch(f"{self.model_class}") as mock_model:
            mock_instance = MagicMock()
            mock_model.return_value = mock_instance

            result = self.repository_class.create(self.valid_data)

            mock_instance.full_clean.assert_called_once()
            mock_instance.save.assert_called_once()

    def test_find_by_id_success(self):
        """Test finding an entity by ID successfully."""
        with patch(f"{self.model_class}.objects") as mock_objects:
            mock_entity = MagicMock()
            mock_objects.get.return_value = mock_entity

            result = self.repository_class.find_by_id(1)

            mock_objects.get.assert_called_once_with(id=1)
            self.assertIsNotNone(result)

    def test_find_by_id_not_found(self):
        """Test finding an entity by ID returns None when not found."""
        with patch(f"{self.model_class}.objects") as mock_objects:
            mock_objects.get.side_effect = ObjectDoesNotExist()

            result = self.repository_class.find_by_id(999)

            self.assertIsNone(result)

    def test_find_all(self):
        """Test finding all entities."""
        with patch(f"{self.model_class}.objects") as mock_objects:
            mock_queryset = [MagicMock(), MagicMock()]
            mock_objects.all.return_value = mock_queryset

            result = self.repository_class.find_all()

            mock_objects.all.assert_called_once()
            self.assertEqual(len(result), 2)


class TestDegreeRepository(GenericRepositoryTestMixin, unittest.TestCase):
    """Test cases for DegreeRepository."""

    def setUp(self):
        """Set up test fixtures."""
        from app.repositories import DegreeRepository

        self.repository_class = DegreeRepository
        self.model_class = "app.repositories.degree.Degree"
        self.valid_data = {"name": "Ingeniería en Sistemas"}


class TestDocumentTypeRepository(GenericRepositoryTestMixin, unittest.TestCase):
    """Test cases for DocumentTypeRepository."""

    def setUp(self):
        """Set up test fixtures."""
        from app.repositories import DocumentTypeRepository

        self.repository_class = DocumentTypeRepository
        self.model_class = "app.repositories.document_type.DocumentType"
        self.valid_data = {"name": "DNI"}


class TestDepartmentRepository(GenericRepositoryTestMixin, unittest.TestCase):
    """Test cases for DepartmentRepository."""

    def setUp(self):
        """Set up test fixtures."""
        from app.repositories import DepartmentRepository

        self.repository_class = DepartmentRepository
        self.model_class = "app.repositories.department.Department"
        self.valid_data = {"name": "Departamento de Computación"}


class TestAreaRepository(GenericRepositoryTestMixin, unittest.TestCase):
    """Test cases for AreaRepository."""

    def setUp(self):
        """Set up test fixtures."""
        from app.repositories import AreaRepository

        self.repository_class = AreaRepository
        self.model_class = "app.repositories.area.Area"
        self.valid_data = {"name": "Área de Sistemas"}


class TestDedicationTypeRepository(GenericRepositoryTestMixin, unittest.TestCase):
    """Test cases for DedicationTypeRepository."""

    def setUp(self):
        """Set up test fixtures."""
        from app.repositories import DedicationTypeRepository

        self.repository_class = DedicationTypeRepository
        self.model_class = "app.repositories.dedication_type.DedicationType"
        self.valid_data = {"name": "Dedicación Exclusiva", "hours": 40}


class TestPositionCategoryRepository(GenericRepositoryTestMixin, unittest.TestCase):
    """Test cases for PositionCategoryRepository."""

    def setUp(self):
        """Set up test fixtures."""
        from app.repositories import PositionCategoryRepository

        self.repository_class = PositionCategoryRepository
        self.model_class = "app.repositories.position_category.PositionCategory"
        self.valid_data = {"name": "Profesor Titular"}


class TestSpecialtyTypeRepository(GenericRepositoryTestMixin, unittest.TestCase):
    """Test cases for SpecialtyTypeRepository."""

    def setUp(self):
        """Set up test fixtures."""
        from app.repositories import SpecialtyTypeRepository

        self.repository_class = SpecialtyTypeRepository
        self.model_class = "app.repositories.specialty_type.SpecialtyType"
        self.valid_data = {"name": "Orientación"}


class TestGroupRepository(GenericRepositoryTestMixin, unittest.TestCase):
    """Test cases for GroupRepository."""

    def setUp(self):
        """Set up test fixtures."""
        from app.repositories import GroupRepository

        self.repository_class = GroupRepository
        self.model_class = "app.repositories.group.Group"
        self.valid_data = {"name": "Grupo A"}


if __name__ == "__main__":
    unittest.main()
