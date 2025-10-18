"""Unit tests for Department repository."""
import unittest
from unittest.mock import patch, MagicMock


class TestDepartmentRepository(unittest.TestCase):
    """Test cases for DepartmentRepository."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_department = MagicMock()
        self.mock_department.id = 1
        self.mock_department.name = 'Departamento de Informática'

    @patch('app.repositories.department.Department')
    def test_create_success(self, mock_model):
        """Test creating a department successfully."""
        from app.repositories import DepartmentRepository
        
        mock_model.objects.create.return_value = self.mock_department
        
        result = DepartmentRepository.create({
            'name': 'Departamento de Informática',
            'faculty': 1
        })
        
        self.assertEqual(result, self.mock_department)

    @patch('app.repositories.department.Department')
    def test_find_by_id(self, mock_model):
        """Test finding department by ID."""
        from app.repositories import DepartmentRepository
        
        mock_model.objects.get.return_value = self.mock_department
        
        result = DepartmentRepository.find_by_id(1)
        
        self.assertEqual(result, self.mock_department)

    @patch('app.repositories.department.Department')
    def test_find_by_faculty(self, mock_model):
        """Test finding departments by faculty."""
        from app.repositories import DepartmentRepository
        
        mock_model.objects.filter.return_value = [self.mock_department]
        
        result = DepartmentRepository.find_by_faculty(1)
        
        self.assertEqual(len(result), 1)

    @patch('app.repositories.department.Department')
    def test_find_all(self, mock_model):
        """Test finding all departments."""
        from app.repositories import DepartmentRepository
        
        mock_model.objects.all.return_value = [self.mock_department]
        
        result = DepartmentRepository.find_all()
        
        self.assertEqual(len(result), 1)

    @patch('app.repositories.department.Department')
    def test_update_success(self, mock_model):
        """Test updating a department successfully."""
        from app.repositories import DepartmentRepository
        
        mock_model.objects.filter.return_value.update.return_value = 1
        mock_model.objects.get.return_value = self.mock_department
        
        result = DepartmentRepository.update(1, {'name': 'Updated'})
        
        self.assertEqual(result, self.mock_department)

    @patch('app.repositories.department.Department')
    def test_delete_success(self, mock_model):
        """Test deleting a department successfully."""
        from app.repositories import DepartmentRepository
        
        mock_model.objects.filter.return_value.delete.return_value = (1, {})
        
        result = DepartmentRepository.delete(1)
        
        self.assertTrue(result)

    @patch('app.repositories.department.Department')
    def test_exists_by_name(self, mock_model):
        """Test checking if department exists by name."""
        from app.repositories import DepartmentRepository
        
        mock_model.objects.filter.return_value.exists.return_value = True
        
        result = DepartmentRepository.exists_by_name('Informática', 1)
        
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
