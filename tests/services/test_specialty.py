"""Unit tests for SpecialtyService."""

import unittest
from unittest.mock import patch, MagicMock


class TestSpecialtyService(unittest.TestCase):
    """Test cases for SpecialtyService."""

    def setUp(self):
        """Set up test fixtures."""
        self.specialty_data = {
            "name": "Computación",
            "faculty_id": 1,
            "specialty_type_id": 1,
        }

        self.mock_specialty = MagicMock()
        self.mock_specialty.id = 1
        self.mock_specialty.name = "Computación"

    @patch("app.services.specialty.SpecialtyRepository")
    def test_create_success(self, mock_repo):
        """Test creating a specialty successfully."""
        from app.services import SpecialtyService

        mock_repo.create.return_value = self.mock_specialty

        result = SpecialtyService.create(self.specialty_data)

        mock_repo.create.assert_called_once_with(self.specialty_data)
        self.assertEqual(result, self.mock_specialty)

    @patch("app.services.specialty.SpecialtyRepository")
    def test_find_by_id_success(self, mock_repo):
        """Test finding a specialty by ID."""
        from app.services import SpecialtyService

        mock_repo.find_by_id.return_value = self.mock_specialty

        result = SpecialtyService.find_by_id(1)

        self.assertEqual(result, self.mock_specialty)

    @patch("app.services.specialty.SpecialtyRepository")
    def test_find_by_faculty(self, mock_repo):
        """Test finding specialties by faculty."""
        from app.services import SpecialtyService

        mock_specialties = [self.mock_specialty]
        mock_repo.find_by_faculty.return_value = mock_specialties

        result = SpecialtyService.find_by_faculty(1)

        self.assertEqual(len(result), 1)

    @patch("app.services.specialty.SpecialtyRepository")
    def test_find_all(self, mock_repo):
        """Test finding all specialties."""
        from app.services import SpecialtyService

        mock_specialties = [self.mock_specialty, MagicMock()]
        mock_repo.find_all.return_value = mock_specialties

        result = SpecialtyService.find_all()

        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()
