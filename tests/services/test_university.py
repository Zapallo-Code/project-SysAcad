"""Unit tests for UniversityService."""
import unittest
from unittest.mock import patch, MagicMock, call
from django.db import transaction


class TestUniversityService(unittest.TestCase):
    """Test cases for UniversityService."""

    def setUp(self):
        """Set up test fixtures."""
        self.university_data = {
            'name': 'Universidad Nacional de Córdoba',
            'acronym': 'UNC'
        }
        
        self.mock_university = MagicMock()
        self.mock_university.id = 1
        self.mock_university.name = 'Universidad Nacional de Córdoba'
        self.mock_university.acronym = 'UNC'

    @patch('app.services.university.UniversityRepository')
    @patch('app.services.university.transaction.atomic')
    def test_create_success(self, mock_atomic, mock_repo):
        """Test creating a university successfully."""
        from app.services import UniversityService
        
        mock_repo.exists_by_name.return_value = False
        mock_repo.exists_by_acronym.return_value = False
        mock_repo.create.return_value = self.mock_university
        mock_atomic.return_value.__enter__ = MagicMock()
        mock_atomic.return_value.__exit__ = MagicMock()
        
        result = UniversityService.create(self.university_data)
        
        mock_repo.exists_by_name.assert_called_once_with('Universidad Nacional de Córdoba')
        mock_repo.exists_by_acronym.assert_called_once_with('UNC')
        mock_repo.create.assert_called_once_with(self.university_data)
        self.assertEqual(result, self.mock_university)

    @patch('app.services.university.UniversityRepository')
    def test_create_duplicate_name(self, mock_repo):
        """Test creating a university with duplicate name raises ValueError."""
        from app.services import UniversityService
        
        mock_repo.exists_by_name.return_value = True
        
        with self.assertRaises(ValueError) as context:
            UniversityService.create(self.university_data)
        
        self.assertIn('already taken', str(context.exception))

    @patch('app.services.university.UniversityRepository')
    def test_create_duplicate_acronym(self, mock_repo):
        """Test creating a university with duplicate acronym raises ValueError."""
        from app.services import UniversityService
        
        mock_repo.exists_by_name.return_value = False
        mock_repo.exists_by_acronym.return_value = True
        
        with self.assertRaises(ValueError) as context:
            UniversityService.create(self.university_data)
        
        self.assertIn('already taken', str(context.exception))

    @patch('app.services.university.UniversityRepository')
    def test_find_by_id_success(self, mock_repo):
        """Test finding a university by ID successfully."""
        from app.services import UniversityService
        
        mock_repo.find_by_id.return_value = self.mock_university
        
        result = UniversityService.find_by_id(1)
        
        mock_repo.find_by_id.assert_called_once_with(1)
        self.assertEqual(result, self.mock_university)

    @patch('app.services.university.UniversityRepository')
    def test_find_by_id_not_found(self, mock_repo):
        """Test finding a non-existent university returns None."""
        from app.services import UniversityService
        
        mock_repo.find_by_id.return_value = None
        
        result = UniversityService.find_by_id(999)
        
        self.assertIsNone(result)

    @patch('app.services.university.UniversityRepository')
    def test_find_by_name_success(self, mock_repo):
        """Test finding a university by name successfully."""
        from app.services import UniversityService
        
        mock_repo.find_by_name.return_value = self.mock_university
        
        result = UniversityService.find_by_name('Universidad Nacional de Córdoba')
        
        mock_repo.find_by_name.assert_called_once_with('Universidad Nacional de Córdoba')
        self.assertEqual(result, self.mock_university)

    @patch('app.services.university.UniversityRepository')
    def test_find_all(self, mock_repo):
        """Test finding all universities."""
        from app.services import UniversityService
        
        mock_universities = [self.mock_university, MagicMock()]
        mock_repo.find_all.return_value = mock_universities
        
        result = UniversityService.find_all()
        
        mock_repo.find_all.assert_called_once()
        self.assertEqual(len(result), 2)

    @patch('app.services.university.UniversityRepository')
    @patch('app.services.university.transaction.atomic')
    def test_update_success(self, mock_atomic, mock_repo):
        """Test updating a university successfully."""
        from app.services import UniversityService
        
        existing = MagicMock()
        existing.id = 1
        existing.name = 'Old Name'
        existing.acronym = 'OLD'
        
        mock_repo.find_by_id.return_value = existing
        mock_repo.exists_by_name.return_value = False
        mock_repo.exists_by_acronym.return_value = False
        mock_repo.update.return_value = self.mock_university
        mock_atomic.return_value.__enter__ = MagicMock()
        mock_atomic.return_value.__exit__ = MagicMock()
        
        update_data = {'name': 'New Name', 'acronym': 'NEW'}
        result = UniversityService.update(1, update_data)
        
        mock_repo.find_by_id.assert_called_once_with(1)
        mock_repo.update.assert_called_once()
        self.assertEqual(result, self.mock_university)

    @patch('app.services.university.UniversityRepository')
    def test_update_not_found(self, mock_repo):
        """Test updating a non-existent university raises ValueError."""
        from app.services import UniversityService
        
        mock_repo.find_by_id.return_value = None
        
        with self.assertRaises(ValueError) as context:
            UniversityService.update(999, self.university_data)
        
        self.assertIn('does not exist', str(context.exception))

    @patch('app.services.university.UniversityRepository')
    def test_update_duplicate_name(self, mock_repo):
        """Test updating with duplicate name raises ValueError."""
        from app.services import UniversityService
        
        existing = MagicMock()
        existing.id = 1
        existing.name = 'Old Name'
        existing.acronym = 'UNC'
        
        mock_repo.find_by_id.return_value = existing
        mock_repo.exists_by_name.return_value = True
        
        update_data = {'name': 'Duplicate Name'}
        
        with self.assertRaises(ValueError) as context:
            UniversityService.update(1, update_data)
        
        self.assertIn('already taken', str(context.exception))

    @patch('app.services.university.UniversityRepository')
    def test_update_duplicate_acronym(self, mock_repo):
        """Test updating with duplicate acronym raises ValueError."""
        from app.services import UniversityService
        
        existing = MagicMock()
        existing.id = 1
        existing.name = 'Universidad Nacional de Córdoba'
        existing.acronym = 'OLD'
        
        mock_repo.find_by_id.return_value = existing
        mock_repo.exists_by_acronym.return_value = True
        
        update_data = {'acronym': 'DUP'}
        
        with self.assertRaises(ValueError) as context:
            UniversityService.update(1, update_data)
        
        self.assertIn('already taken', str(context.exception))

    @patch('app.services.university.UniversityRepository')
    @patch('app.services.university.transaction.atomic')
    def test_delete_by_id_success(self, mock_atomic, mock_repo):
        """Test deleting a university successfully."""
        from app.services import UniversityService
        
        mock_repo.exists_by_id.return_value = True
        mock_repo.delete_by_id.return_value = True
        mock_atomic.return_value.__enter__ = MagicMock()
        mock_atomic.return_value.__exit__ = MagicMock()
        
        result = UniversityService.delete_by_id(1)
        
        mock_repo.exists_by_id.assert_called_once_with(1)
        mock_repo.delete_by_id.assert_called_once_with(1)
        self.assertTrue(result)

    @patch('app.services.university.UniversityRepository')
    def test_delete_by_id_not_found(self, mock_repo):
        """Test deleting a non-existent university raises ValueError."""
        from app.services import UniversityService
        
        mock_repo.exists_by_id.return_value = False
        
        with self.assertRaises(ValueError) as context:
            UniversityService.delete_by_id(999)
        
        self.assertIn('does not exist', str(context.exception))

    @patch('app.services.university.logger')
    @patch('app.services.university.UniversityRepository')
    def test_logging_on_create(self, mock_repo, mock_logger):
        """Test that logging occurs during create operation."""
        from app.services import UniversityService
        
        mock_repo.exists_by_name.return_value = False
        mock_repo.exists_by_acronym.return_value = False
        mock_repo.create.return_value = self.mock_university
        
        UniversityService.create(self.university_data)
        
        self.assertTrue(mock_logger.info.called)

    @patch('app.services.university.logger')
    @patch('app.services.university.UniversityRepository')
    def test_logging_on_error(self, mock_repo, mock_logger):
        """Test that error logging occurs on exceptions."""
        from app.services import UniversityService
        
        mock_repo.exists_by_name.return_value = True
        
        try:
            UniversityService.create(self.university_data)
        except ValueError:
            pass
        
        self.assertTrue(mock_logger.error.called)


if __name__ == '__main__':
    unittest.main()
