"""Unit tests for SubjectRepository."""
import unittest
from unittest.mock import patch, MagicMock
from django.core.exceptions import ObjectDoesNotExist


class TestSubjectRepository(unittest.TestCase):
    """Test cases for SubjectRepository."""

    def setUp(self):
        """Set up test fixtures."""
        self.subject_data = {
            'name': 'Algoritmos y Estructuras de Datos',
            'code': 'AED',
            'plan_id': 1,
            'area_id': 1
        }
        
        self.mock_subject = MagicMock()
        self.mock_subject.id = 1
        self.mock_subject.name = 'Algoritmos y Estructuras de Datos'
        self.mock_subject.code = 'AED'

    @patch('app.repositories.subject.Subject')
    def test_create_success(self, mock_model):
        """Test creating a subject successfully."""
        from app.repositories import SubjectRepository
        
        mock_instance = MagicMock()
        mock_model.return_value = mock_instance
        
        result = SubjectRepository.create(self.subject_data)
        
        mock_instance.full_clean.assert_called_once()
        mock_instance.save.assert_called_once()

    @patch('app.repositories.subject.Subject.objects')
    def test_find_by_id_success(self, mock_objects):
        """Test finding a subject by ID."""
        from app.repositories import SubjectRepository
        
        mock_objects.get.return_value = self.mock_subject
        
        result = SubjectRepository.find_by_id(1)
        
        self.assertEqual(result, self.mock_subject)

    @patch('app.repositories.subject.Subject.objects')
    def test_find_by_code(self, mock_objects):
        """Test finding a subject by code."""
        from app.repositories import SubjectRepository
        
        mock_objects.get.return_value = self.mock_subject
        
        result = SubjectRepository.find_by_code('AED')
        
        mock_objects.get.assert_called_once_with(code='AED')

    @patch('app.repositories.subject.Subject.objects')
    def test_find_by_plan(self, mock_objects):
        """Test finding subjects by plan."""
        from app.repositories import SubjectRepository
        
        mock_queryset = [self.mock_subject]
        mock_objects.filter.return_value = mock_queryset
        
        result = SubjectRepository.find_by_plan(1)
        
        self.assertEqual(len(result), 1)

    @patch('app.repositories.subject.Subject.objects')
    def test_find_by_area(self, mock_objects):
        """Test finding subjects by area."""
        from app.repositories import SubjectRepository
        
        mock_queryset = [self.mock_subject]
        mock_objects.filter.return_value = mock_queryset
        
        result = SubjectRepository.find_by_area(1)
        
        self.assertEqual(len(result), 1)

    @patch('app.repositories.subject.Subject.objects')
    def test_search_by_name(self, mock_objects):
        """Test searching subjects by name."""
        from app.repositories import SubjectRepository
        
        mock_queryset = [self.mock_subject]
        mock_objects.filter.return_value = mock_queryset
        
        result = SubjectRepository.search_by_name('Algoritmos')
        
        self.assertEqual(len(result), 1)

    @patch('app.repositories.subject.Subject.objects')
    def test_exists_by_code(self, mock_objects):
        """Test checking if subject exists by code."""
        from app.repositories import SubjectRepository
        
        mock_filter = MagicMock()
        mock_filter.return_value.exists.return_value = True
        mock_objects.filter = mock_filter
        
        result = SubjectRepository.exists_by_code('AED')
        
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
