"""Unit tests for FacultyRepository."""
import unittest
from unittest.mock import patch, MagicMock
from django.core.exceptions import ObjectDoesNotExist, ValidationError


class TestFacultyRepository(unittest.TestCase):
    """Test cases for FacultyRepository."""

    def setUp(self):
        """Set up test fixtures."""
        self.faculty_data = {
            'name': 'Facultad de Ciencias Exactas',
            'university_id': 1
        }
        
        self.mock_faculty = MagicMock()
        self.mock_faculty.id = 1
        self.mock_faculty.name = 'Facultad de Ciencias Exactas'

    @patch('app.repositories.faculty.Faculty')
    def test_create_success(self, mock_faculty_model):
        """Test creating a faculty successfully."""
        from app.repositories import FacultyRepository
        
        mock_instance = MagicMock()
        mock_faculty_model.return_value = mock_instance
        
        result = FacultyRepository.create(self.faculty_data)
        
        mock_instance.full_clean.assert_called_once()
        mock_instance.save.assert_called_once()

    @patch('app.repositories.faculty.Faculty.objects')
    def test_find_by_id_success(self, mock_objects):
        """Test finding a faculty by ID successfully."""
        from app.repositories import FacultyRepository
        
        mock_objects.get.return_value = self.mock_faculty
        
        result = FacultyRepository.find_by_id(1)
        
        mock_objects.get.assert_called_once_with(id=1)
        self.assertEqual(result, self.mock_faculty)

    @patch('app.repositories.faculty.Faculty.objects')
    def test_find_by_id_not_found(self, mock_objects):
        """Test finding a faculty by ID returns None when not found."""
        from app.repositories import FacultyRepository
        
        mock_objects.get.side_effect = ObjectDoesNotExist()
        
        result = FacultyRepository.find_by_id(999)
        
        self.assertIsNone(result)

    @patch('app.repositories.faculty.Faculty.objects')
    def test_find_all(self, mock_objects):
        """Test finding all faculties."""
        from app.repositories import FacultyRepository
        
        mock_queryset = [self.mock_faculty, MagicMock()]
        mock_objects.all.return_value = mock_queryset
        
        result = FacultyRepository.find_all()
        
        mock_objects.all.assert_called_once()
        self.assertEqual(len(result), 2)

    @patch('app.repositories.faculty.Faculty.objects')
    def test_find_by_university(self, mock_objects):
        """Test finding faculties by university."""
        from app.repositories import FacultyRepository
        
        mock_queryset = [self.mock_faculty]
        mock_filter = MagicMock()
        mock_filter.return_value = mock_queryset
        mock_objects.filter = mock_filter
        
        result = FacultyRepository.find_by_university(1)
        
        self.assertEqual(len(result), 1)

    @patch('app.repositories.faculty.Faculty')
    def test_update_success(self, mock_faculty_model):
        """Test updating a faculty successfully."""
        from app.repositories import FacultyRepository
        
        result = FacultyRepository.update(self.mock_faculty)
        
        self.mock_faculty.full_clean.assert_called_once()
        self.mock_faculty.save.assert_called_once()

    @patch('app.repositories.faculty.FacultyRepository.find_by_id')
    def test_delete_by_id_success(self, mock_find):
        """Test deleting a faculty by ID successfully."""
        from app.repositories import FacultyRepository
        
        mock_find.return_value = self.mock_faculty
        
        result = FacultyRepository.delete_by_id(1)
        
        mock_find.assert_called_once_with(1)
        self.mock_faculty.delete.assert_called_once()
        self.assertTrue(result)

    @patch('app.repositories.faculty.Faculty.objects')
    def test_exists_by_id(self, mock_objects):
        """Test checking if faculty exists by ID."""
        from app.repositories import FacultyRepository
        
        mock_filter = MagicMock()
        mock_filter.return_value.exists.return_value = True
        mock_objects.filter = mock_filter
        
        result = FacultyRepository.exists_by_id(1)
        
        self.assertTrue(result)

    @patch('app.repositories.faculty.Faculty.objects')
    def test_count(self, mock_objects):
        """Test counting faculties."""
        from app.repositories import FacultyRepository
        
        mock_objects.count.return_value = 3
        
        result = FacultyRepository.count()
        
        self.assertEqual(result, 3)


if __name__ == '__main__':
    unittest.main()
