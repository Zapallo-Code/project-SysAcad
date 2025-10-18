"""Unit tests for SpecialtyRepository."""
import unittest
from unittest.mock import patch, MagicMock
from django.core.exceptions import ObjectDoesNotExist


class TestSpecialtyRepository(unittest.TestCase):
    """Test cases for SpecialtyRepository."""

    def setUp(self):
        """Set up test fixtures."""
        self.specialty_data = {
            'name': 'Computación',
            'faculty_id': 1,
            'specialty_type_id': 1
        }
        
        self.mock_specialty = MagicMock()
        self.mock_specialty.id = 1
        self.mock_specialty.name = 'Computación'

    @patch('app.repositories.specialty.Specialty')
    def test_create_success(self, mock_model):
        """Test creating a specialty successfully."""
        from app.repositories import SpecialtyRepository
        
        mock_instance = MagicMock()
        mock_model.return_value = mock_instance
        
        result = SpecialtyRepository.create(self.specialty_data)
        
        mock_instance.full_clean.assert_called_once()
        mock_instance.save.assert_called_once()

    @patch('app.repositories.specialty.Specialty.objects')
    def test_find_by_id_success(self, mock_objects):
        """Test finding a specialty by ID."""
        from app.repositories import SpecialtyRepository
        
        mock_objects.get.return_value = self.mock_specialty
        
        result = SpecialtyRepository.find_by_id(1)
        
        self.assertEqual(result, self.mock_specialty)

    @patch('app.repositories.specialty.Specialty.objects')
    def test_find_by_faculty(self, mock_objects):
        """Test finding specialties by faculty."""
        from app.repositories import SpecialtyRepository
        
        mock_queryset = [self.mock_specialty]
        mock_objects.filter.return_value = mock_queryset
        
        result = SpecialtyRepository.find_by_faculty(1)
        
        self.assertEqual(len(result), 1)

    @patch('app.repositories.specialty.Specialty.objects')
    def test_find_all(self, mock_objects):
        """Test finding all specialties."""
        from app.repositories import SpecialtyRepository
        
        mock_queryset = [self.mock_specialty, MagicMock()]
        mock_objects.all.return_value = mock_queryset
        
        result = SpecialtyRepository.find_all()
        
        self.assertEqual(len(result), 2)


if __name__ == '__main__':
    unittest.main()
