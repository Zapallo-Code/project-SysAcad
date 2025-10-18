"""Unit tests for Department service."""
import unittest
from unittest.mock import patch, MagicMock


class TestDepartmentService(unittest.TestCase):
    """Test cases for DepartmentService."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_department = MagicMock()
        self.mock_department.id = 1
        self.mock_department.name = 'Departamento de Informática'

    @patch('app.services.department.DepartmentRepository')
    def test_create_success(self, mock_repo):
        """Test creating a department successfully."""
        from app.services import DepartmentService
        
        mock_repo.create.return_value = self.mock_department
        
        result = DepartmentService.create({
            'name': 'Departamento de Informática',
            'faculty': 1
        })
        
        self.assertEqual(result, self.mock_department)

    @patch('app.services.department.DepartmentRepository')
    def test_find_by_id(self, mock_repo):
        """Test finding department by ID."""
        from app.services import DepartmentService
        
        mock_repo.find_by_id.return_value = self.mock_department
        
        result = DepartmentService.find_by_id(1)
        
        self.assertEqual(result, self.mock_department)

    @patch('app.services.department.DepartmentRepository')
    def test_find_by_faculty(self, mock_repo):
        """Test finding departments by faculty."""
        from app.services import DepartmentService
        
        mock_repo.find_by_faculty.return_value = [self.mock_department]
        
        result = DepartmentService.find_by_faculty(1)
        
        self.assertEqual(len(result), 1)

    @patch('app.services.department.DepartmentRepository')
    def test_find_all(self, mock_repo):
        """Test finding all departments."""
        from app.services import DepartmentService
        
        mock_repo.find_all.return_value = [self.mock_department]
        
        result = DepartmentService.find_all()
        
        self.assertEqual(len(result), 1)

    @patch('app.services.department.DepartmentRepository')
    def test_update_success(self, mock_repo):
        """Test updating a department successfully."""
        from app.services import DepartmentService
        
        mock_repo.update.return_value = self.mock_department
        
        result = DepartmentService.update(1, {'name': 'Updated Department'})
        
        self.assertEqual(result, self.mock_department)

    @patch('app.services.department.DepartmentRepository')
    def test_delete_success(self, mock_repo):
        """Test deleting a department successfully."""
        from app.services import DepartmentService
        
        mock_repo.delete.return_value = True
        
        result = DepartmentService.delete(1)
        
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
