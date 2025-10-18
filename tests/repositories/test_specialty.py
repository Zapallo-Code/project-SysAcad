"""Unit tests for SpecialtyRepository."""

import unittest
from unittest.mock import patch, MagicMock
from django.core.exceptions import ObjectDoesNotExist


class TestSpecialtyRepository(unittest.TestCase):
    """Test cases for SpecialtyRepository."""

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

    @patch("app.repositories.specialty.Specialty")
    def test_create_success(self, mock_model):
        """Test creating a specialty successfully."""
        from app.repositories import SpecialtyRepository

        mock_instance = MagicMock()
        mock_model.return_value = mock_instance

        result = SpecialtyRepository.create(self.specialty_data)

        mock_instance.full_clean.assert_called_once()
        mock_instance.save.assert_called_once()

    @patch("app.repositories.specialty.Specialty.objects")
    def test_find_by_id_success(self, mock_objects):
        """Test finding a specialty by ID."""
        from app.repositories import SpecialtyRepository

        mock_select_related = MagicMock()
        mock_select_related.get.return_value = self.mock_specialty
        mock_objects.select_related.return_value = mock_select_related

        result = SpecialtyRepository.find_by_id(1)

        mock_objects.select_related.assert_called_once_with("specialty_type", "faculty")
        mock_select_related.get.assert_called_once_with(id=1)
        self.assertEqual(result, self.mock_specialty)

    @patch("app.repositories.specialty.Specialty.objects")
    def test_find_by_faculty(self, mock_objects):
        """Test finding specialties by faculty."""
        from app.repositories import SpecialtyRepository

        mock_queryset = [self.mock_specialty]
        mock_filter = MagicMock()
        mock_filter.select_related.return_value = mock_queryset
        mock_objects.filter.return_value = mock_filter

        result = SpecialtyRepository.find_by_faculty(1)

        self.assertEqual(len(result), 1)

    @patch("app.repositories.specialty.Specialty.objects")
    def test_find_all(self, mock_objects):
        """Test finding all specialties."""
        from app.repositories import SpecialtyRepository

        mock_queryset = [self.mock_specialty, MagicMock()]
        mock_select_related = MagicMock()
        mock_select_related.all.return_value = mock_queryset
        mock_objects.select_related.return_value = mock_select_related

        result = SpecialtyRepository.find_all()

        mock_objects.select_related.assert_called_once_with("specialty_type", "faculty")
        mock_select_related.all.assert_called_once()
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()
