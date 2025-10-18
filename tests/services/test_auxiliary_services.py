"""Unit tests for DedicationType service."""

import unittest
from unittest.mock import patch, MagicMock


class TestDedicationTypeService(unittest.TestCase):
    """Test cases for DedicationTypeService."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_dedication = MagicMock()
        self.mock_dedication.id = 1
        self.mock_dedication.name = "Dedicación Exclusiva"
        self.mock_dedication.hours = 40

    @patch("app.services.dedication_type.DedicationTypeRepository")
    def test_create_success(self, mock_repo):
        """Test creating a dedication type successfully."""
        from app.services import DedicationTypeService

        mock_repo.create.return_value = self.mock_dedication

        result = DedicationTypeService.create(
            {"name": "Dedicación Exclusiva", "hours": 40}
        )

        self.assertEqual(result, self.mock_dedication)
        mock_repo.create.assert_called_once()

    @patch("app.services.dedication_type.DedicationTypeRepository")
    def test_find_by_id(self, mock_repo):
        """Test finding dedication type by ID."""
        from app.services import DedicationTypeService

        mock_repo.find_by_id.return_value = self.mock_dedication

        result = DedicationTypeService.find_by_id(1)

        self.assertEqual(result, self.mock_dedication)

    @patch("app.services.dedication_type.DedicationTypeRepository")
    def test_find_all(self, mock_repo):
        """Test finding all dedication types."""
        from app.services import DedicationTypeService

        mock_repo.find_all.return_value = [self.mock_dedication]

        result = DedicationTypeService.find_all()

        self.assertEqual(len(result), 1)

    @patch("app.services.dedication_type.DedicationTypeRepository")
    def test_update_success(self, mock_repo):
        """Test updating a dedication type successfully."""
        from app.services import DedicationTypeService

        mock_repo.update.return_value = self.mock_dedication

        result = DedicationTypeService.update(1, {"hours": 45})

        self.assertEqual(result, self.mock_dedication)

    @patch("app.services.dedication_type.DedicationTypeRepository")
    def test_delete_success(self, mock_repo):
        """Test deleting a dedication type successfully."""
        from app.services import DedicationTypeService

        mock_repo.delete.return_value = True

        result = DedicationTypeService.delete(1)

        self.assertTrue(result)


class TestPositionCategoryService(unittest.TestCase):
    """Test cases for PositionCategoryService."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_category = MagicMock()
        self.mock_category.id = 1
        self.mock_category.name = "Profesor Titular"

    @patch("app.services.position_category.PositionCategoryRepository")
    def test_create_success(self, mock_repo):
        """Test creating a position category successfully."""
        from app.services import PositionCategoryService

        mock_repo.create.return_value = self.mock_category

        result = PositionCategoryService.create({"name": "Profesor Titular"})

        self.assertEqual(result, self.mock_category)

    @patch("app.services.position_category.PositionCategoryRepository")
    def test_find_all(self, mock_repo):
        """Test finding all position categories."""
        from app.services import PositionCategoryService

        mock_repo.find_all.return_value = [self.mock_category]

        result = PositionCategoryService.find_all()

        self.assertEqual(len(result), 1)


class TestSpecialtyTypeService(unittest.TestCase):
    """Test cases for SpecialtyTypeService."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_specialty_type = MagicMock()
        self.mock_specialty_type.id = 1
        self.mock_specialty_type.name = "Licenciatura"

    @patch("app.services.specialty_type.SpecialtyTypeRepository")
    def test_create_success(self, mock_repo):
        """Test creating a specialty type successfully."""
        from app.services import SpecialtyTypeService

        mock_repo.create.return_value = self.mock_specialty_type

        result = SpecialtyTypeService.create({"name": "Licenciatura"})

        self.assertEqual(result, self.mock_specialty_type)

    @patch("app.services.specialty_type.SpecialtyTypeRepository")
    def test_find_all(self, mock_repo):
        """Test finding all specialty types."""
        from app.services import SpecialtyTypeService

        mock_repo.find_all.return_value = [self.mock_specialty_type]

        result = SpecialtyTypeService.find_all()

        self.assertEqual(len(result), 1)


if __name__ == "__main__":
    unittest.main()
