"""Generic unit tests for simple services."""

import unittest
from unittest.mock import patch, MagicMock


class GenericServiceTestMixin:
    """Mixin for generic service tests."""

    service_class = None
    repository_path = None
    valid_data = None

    def test_create_success(self):
        """Test creating an entity successfully."""
        with patch(f"{self.repository_path}") as mock_repo:
            mock_entity = MagicMock()
            mock_entity.id = 1
            mock_repo.exists_by_name.return_value = False
            mock_repo.create.return_value = mock_entity

            result = self.service_class.create(self.valid_data)

            mock_repo.create.assert_called_once_with(self.valid_data)
            self.assertIsNotNone(result)

    def test_find_by_id_success(self):
        """Test finding an entity by ID successfully."""
        with patch(f"{self.repository_path}") as mock_repo:
            mock_entity = MagicMock()
            mock_repo.find_by_id.return_value = mock_entity

            result = self.service_class.find_by_id(1)

            mock_repo.find_by_id.assert_called_once_with(1)
            self.assertIsNotNone(result)

    def test_find_by_id_not_found(self):
        """Test finding an entity by ID returns None when not found."""
        with patch(f"{self.repository_path}") as mock_repo:
            mock_repo.find_by_id.return_value = None

            result = self.service_class.find_by_id(999)

            self.assertIsNone(result)

    def test_find_all(self):
        """Test finding all entities."""
        with patch(f"{self.repository_path}") as mock_repo:
            mock_entities = [MagicMock(), MagicMock()]
            mock_repo.find_all.return_value = mock_entities

            result = self.service_class.find_all()

            mock_repo.find_all.assert_called_once()
            self.assertEqual(len(result), 2)


class TestDegreeService(GenericServiceTestMixin, unittest.TestCase):
    """Test cases for DegreeService."""

    def setUp(self):
        """Set up test fixtures."""
        from app.services import DegreeService

        self.service_class = DegreeService
        self.repository_path = "app.services.degree.DegreeRepository"
        self.valid_data = {"name": "Ingeniería en Sistemas"}


class TestDocumentTypeService(GenericServiceTestMixin, unittest.TestCase):
    """Test cases for DocumentTypeService."""

    def setUp(self):
        """Set up test fixtures."""
        from app.services import DocumentTypeService

        self.service_class = DocumentTypeService
        self.repository_path = "app.services.document_type.DocumentTypeRepository"
        self.valid_data = {"name": "DNI"}


class TestDepartmentService(GenericServiceTestMixin, unittest.TestCase):
    """Test cases for DepartmentService."""

    def setUp(self):
        """Set up test fixtures."""
        from app.services import DepartmentService

        self.service_class = DepartmentService
        self.repository_path = "app.services.department.DepartmentRepository"
        self.valid_data = {"name": "Departamento de Computación"}


class TestAreaService(GenericServiceTestMixin, unittest.TestCase):
    """Test cases for AreaService."""

    def setUp(self):
        """Set up test fixtures."""
        from app.services import AreaService

        self.service_class = AreaService
        self.repository_path = "app.services.area.AreaRepository"
        self.valid_data = {"name": "Área de Sistemas"}


class TestDedicationTypeService(GenericServiceTestMixin, unittest.TestCase):
    """Test cases for DedicationTypeService."""

    def setUp(self):
        """Set up test fixtures."""
        from app.services import DedicationTypeService

        self.service_class = DedicationTypeService
        self.repository_path = "app.services.dedication_type.DedicationTypeRepository"
        self.valid_data = {"name": "Dedicación Exclusiva", "hours": 40}


class TestPositionCategoryService(GenericServiceTestMixin, unittest.TestCase):
    """Test cases for PositionCategoryService."""

    def setUp(self):
        """Set up test fixtures."""
        from app.services import PositionCategoryService

        self.service_class = PositionCategoryService
        self.repository_path = (
            "app.services.position_category.PositionCategoryRepository"
        )
        self.valid_data = {"name": "Profesor Titular"}


class TestSpecialtyTypeService(GenericServiceTestMixin, unittest.TestCase):
    """Test cases for SpecialtyTypeService."""

    def setUp(self):
        """Set up test fixtures."""
        from app.services import SpecialtyTypeService

        self.service_class = SpecialtyTypeService
        self.repository_path = "app.services.specialty_type.SpecialtyTypeRepository"
        self.valid_data = {"name": "Orientación"}


class TestGroupService(GenericServiceTestMixin, unittest.TestCase):
    """Test cases for GroupService."""

    def setUp(self):
        """Set up test fixtures."""
        from app.services import GroupService

        self.service_class = GroupService
        self.repository_path = "app.services.group.GroupRepository"
        self.valid_data = {"name": "Grupo A"}


if __name__ == "__main__":
    unittest.main()
