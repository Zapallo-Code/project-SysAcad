"""Unit tests for UniversityRepository."""

import unittest
from unittest.mock import patch, MagicMock, call
from django.core.exceptions import ObjectDoesNotExist, ValidationError


class TestUniversityRepository(unittest.TestCase):
    """Test cases for UniversityRepository."""

    def setUp(self):
        """Set up test fixtures."""
        self.university_data = {
            "name": "Universidad Nacional de Córdoba",
            "acronym": "UNC",
        }

        self.mock_university = MagicMock()
        self.mock_university.id = 1
        self.mock_university.name = "Universidad Nacional de Córdoba"
        self.mock_university.acronym = "UNC"

    @patch("app.repositories.university.University")
    def test_create_success(self, mock_university_model):
        """Test creating a university successfully."""
        from app.repositories import UniversityRepository

        mock_instance = MagicMock()
        mock_university_model.return_value = mock_instance

        result = UniversityRepository.create(self.university_data)

        mock_university_model.assert_called_once_with(**self.university_data)
        mock_instance.full_clean.assert_called_once()
        mock_instance.save.assert_called_once()
        self.assertEqual(result, mock_instance)

    @patch("app.repositories.university.University")
    def test_create_validation_error(self, mock_university_model):
        """Test create raises ValidationError on invalid data."""
        from app.repositories import UniversityRepository

        mock_instance = MagicMock()
        mock_instance.full_clean.side_effect = ValidationError("Invalid data")
        mock_university_model.return_value = mock_instance

        with self.assertRaises(ValidationError):
            UniversityRepository.create(self.university_data)

    @patch("app.repositories.university.University.objects")
    def test_find_by_id_success(self, mock_objects):
        """Test finding a university by ID successfully."""
        from app.repositories import UniversityRepository

        mock_objects.get.return_value = self.mock_university

        result = UniversityRepository.find_by_id(1)

        mock_objects.get.assert_called_once_with(id=1)
        self.assertEqual(result, self.mock_university)

    @patch("app.repositories.university.University.objects")
    def test_find_by_id_not_found(self, mock_objects):
        """Test finding a university by ID returns None when not found."""
        from app.repositories import UniversityRepository

        mock_objects.get.side_effect = ObjectDoesNotExist()

        result = UniversityRepository.find_by_id(999)

        self.assertIsNone(result)

    @patch("app.repositories.university.University.objects")
    def test_find_by_acronym_success(self, mock_objects):
        """Test finding a university by acronym successfully."""
        from app.repositories import UniversityRepository

        mock_objects.get.return_value = self.mock_university

        result = UniversityRepository.find_by_acronym("UNC")

        mock_objects.get.assert_called_once_with(acronym="UNC")
        self.assertEqual(result, self.mock_university)

    @patch("app.repositories.university.University.objects")
    def test_find_by_acronym_not_found(self, mock_objects):
        """Test finding a university by acronym returns None when not found."""
        from app.repositories import UniversityRepository

        mock_objects.get.side_effect = ObjectDoesNotExist()

        result = UniversityRepository.find_by_acronym("NONEXISTENT")

        self.assertIsNone(result)

    @patch("app.repositories.university.University.objects")
    def test_find_by_name_success(self, mock_objects):
        """Test finding a university by name successfully."""
        from app.repositories import UniversityRepository

        mock_objects.get.return_value = self.mock_university

        result = UniversityRepository.find_by_name("Universidad Nacional de Córdoba")

        mock_objects.get.assert_called_once_with(name="Universidad Nacional de Córdoba")
        self.assertEqual(result, self.mock_university)

    @patch("app.repositories.university.University.objects")
    def test_find_all(self, mock_objects):
        """Test finding all universities."""
        from app.repositories import UniversityRepository

        mock_queryset = [self.mock_university, MagicMock()]
        mock_objects.all.return_value = mock_queryset

        result = UniversityRepository.find_all()

        mock_objects.all.assert_called_once()
        self.assertEqual(len(result), 2)

    @patch("app.repositories.university.University.objects")
    def test_search_by_name(self, mock_objects):
        """Test searching universities by name."""
        from app.repositories import UniversityRepository

        mock_queryset = [self.mock_university]
        mock_filter = MagicMock()
        mock_filter.return_value = mock_queryset
        mock_objects.filter = mock_filter

        result = UniversityRepository.search_by_name("Nacional")

        mock_objects.filter.assert_called_once_with(name__icontains="Nacional")
        self.assertEqual(len(result), 1)

    @patch("app.repositories.university.University")
    def test_update_success(self, mock_university_model):
        """Test updating a university successfully."""
        from app.repositories import UniversityRepository

        result = UniversityRepository.update(self.mock_university)

        self.mock_university.full_clean.assert_called_once()
        self.mock_university.save.assert_called_once()
        self.assertEqual(result, self.mock_university)

    @patch("app.repositories.university.UniversityRepository.find_by_id")
    def test_delete_by_id_success(self, mock_find):
        """Test deleting a university by ID successfully."""
        from app.repositories import UniversityRepository

        mock_find.return_value = self.mock_university

        result = UniversityRepository.delete_by_id(1)

        mock_find.assert_called_once_with(1)
        self.mock_university.delete.assert_called_once()
        self.assertTrue(result)

    @patch("app.repositories.university.UniversityRepository.find_by_id")
    def test_delete_by_id_not_found(self, mock_find):
        """Test deleting a non-existent university returns False."""
        from app.repositories import UniversityRepository

        mock_find.return_value = None

        result = UniversityRepository.delete_by_id(999)

        self.assertFalse(result)

    @patch("app.repositories.university.University.objects")
    def test_exists_by_id(self, mock_objects):
        """Test checking if university exists by ID."""
        from app.repositories import UniversityRepository

        mock_filter = MagicMock()
        mock_filter.return_value.exists.return_value = True
        mock_objects.filter = mock_filter

        result = UniversityRepository.exists_by_id(1)

        mock_objects.filter.assert_called_once_with(id=1)
        self.assertTrue(result)

    @patch("app.repositories.university.University.objects")
    def test_exists_by_acronym(self, mock_objects):
        """Test checking if university exists by acronym."""
        from app.repositories import UniversityRepository

        mock_filter = MagicMock()
        mock_filter.return_value.exists.return_value = True
        mock_objects.filter = mock_filter

        result = UniversityRepository.exists_by_acronym("UNC")

        mock_objects.filter.assert_called_once_with(acronym="UNC")
        self.assertTrue(result)

    @patch("app.repositories.university.University.objects")
    def test_exists_by_name(self, mock_objects):
        """Test checking if university exists by name."""
        from app.repositories import UniversityRepository

        mock_filter = MagicMock()
        mock_filter.return_value.exists.return_value = False
        mock_objects.filter = mock_filter

        result = UniversityRepository.exists_by_name("Nonexistent")

        mock_objects.filter.assert_called_once_with(name="Nonexistent")
        self.assertFalse(result)

    @patch("app.repositories.university.University.objects")
    def test_count(self, mock_objects):
        """Test counting universities."""
        from app.repositories import UniversityRepository

        mock_objects.count.return_value = 5

        result = UniversityRepository.count()

        mock_objects.count.assert_called_once()
        self.assertEqual(result, 5)

    @patch("app.repositories.university.University.objects")
    def test_find_with_relations(self, mock_objects):
        """Test finding university with relations."""
        from app.repositories import UniversityRepository

        mock_prefetch = MagicMock()
        mock_prefetch.get.return_value = self.mock_university
        mock_objects.prefetch_related.return_value = mock_prefetch

        result = UniversityRepository.find_with_relations(1)

        mock_objects.prefetch_related.assert_called_once_with(
            "faculties", "faculties__specialties"
        )
        mock_prefetch.get.assert_called_once_with(id=1)
        self.assertEqual(result, self.mock_university)


if __name__ == "__main__":
    unittest.main()
