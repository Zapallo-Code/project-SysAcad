"""Unit tests for FacultyService."""

import unittest
from unittest.mock import patch, MagicMock


class TestFacultyService(unittest.TestCase):
    """Test cases for FacultyService."""

    def setUp(self):
        """Set up test fixtures."""
        self.faculty_data = {"name": "Facultad de Ciencias Exactas", "university_id": 1}

        self.mock_faculty = MagicMock()
        self.mock_faculty.id = 1
        self.mock_faculty.name = "Facultad de Ciencias Exactas"

    @patch("app.services.faculty.FacultyRepository")
    @patch("app.services.faculty.transaction.atomic")
    def test_create_success(self, mock_atomic, mock_repo):
        """Test creating a faculty successfully."""
        from app.services import FacultyService

        mock_repo.exists_by_name.return_value = False
        mock_repo.create.return_value = self.mock_faculty
        mock_atomic.return_value.__enter__ = MagicMock()
        mock_atomic.return_value.__exit__ = MagicMock()

        result = FacultyService.create(self.faculty_data)

        mock_repo.create.assert_called_once_with(self.faculty_data)
        self.assertEqual(result, self.mock_faculty)

    @patch("app.services.faculty.FacultyRepository")
    def test_create_duplicate_name(self, mock_repo):
        """Test creating a faculty with duplicate name raises ValueError."""
        from app.services import FacultyService

        mock_repo.exists_by_name.return_value = True

        with self.assertRaises(ValueError):
            FacultyService.create(self.faculty_data)

    @patch("app.services.faculty.FacultyRepository")
    def test_find_by_id_success(self, mock_repo):
        """Test finding a faculty by ID."""
        from app.services import FacultyService

        mock_repo.find_by_id.return_value = self.mock_faculty

        result = FacultyService.find_by_id(1)

        self.assertEqual(result, self.mock_faculty)

    @patch("app.services.faculty.FacultyRepository")
    def test_find_by_university(self, mock_repo):
        """Test finding faculties by university."""
        from app.services import FacultyService

        mock_faculties = [self.mock_faculty]
        mock_repo.find_by_university.return_value = mock_faculties

        result = FacultyService.find_by_university(1)

        self.assertEqual(len(result), 1)

    @patch("app.services.faculty.FacultyRepository")
    def test_find_all(self, mock_repo):
        """Test finding all faculties."""
        from app.services import FacultyService

        mock_faculties = [self.mock_faculty, MagicMock()]
        mock_repo.find_all.return_value = mock_faculties

        result = FacultyService.find_all()

        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()
