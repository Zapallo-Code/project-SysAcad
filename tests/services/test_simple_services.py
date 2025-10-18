"""Unit tests for simple model services: Degree, DocumentType, Department, Area."""
import unittest
from unittest.mock import patch, MagicMock


class TestDegreeService(unittest.TestCase):
    """Test cases for DegreeService."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_degree = MagicMock()
        self.mock_degree.id = 1
        self.mock_degree.name = 'Licenciatura'

    @patch('app.services.degree.DegreeRepository')
    def test_create_success(self, mock_repo):
        """Test creating a degree successfully."""
        from app.services import DegreeService
        
        mock_repo.create.return_value = self.mock_degree
        
        result = DegreeService.create({'name': 'Licenciatura'})
        
        self.assertEqual(result, self.mock_degree)
        mock_repo.create.assert_called_once()

    @patch('app.services.degree.DegreeRepository')
    def test_find_all(self, mock_repo):
        """Test finding all degrees."""
        from app.services import DegreeService
        
        mock_repo.find_all.return_value = [self.mock_degree]
        
        result = DegreeService.find_all()
        
        self.assertEqual(len(result), 1)


class TestDocumentTypeService(unittest.TestCase):
    """Test cases for DocumentTypeService."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_doc_type = MagicMock()
        self.mock_doc_type.id = 1
        self.mock_doc_type.name = 'DNI'

    @patch('app.services.document_type.DocumentTypeRepository')
    def test_create_success(self, mock_repo):
        """Test creating a document type successfully."""
        from app.services import DocumentTypeService
        
        mock_repo.create.return_value = self.mock_doc_type
        
        result = DocumentTypeService.create({'name': 'DNI'})
        
        self.assertEqual(result, self.mock_doc_type)

    @patch('app.services.document_type.DocumentTypeRepository')
    def test_find_by_name(self, mock_repo):
        """Test finding document type by name."""
        from app.services import DocumentTypeService
        
        mock_repo.find_by_name.return_value = self.mock_doc_type
        
        result = DocumentTypeService.find_by_name('DNI')
        
        self.assertEqual(result, self.mock_doc_type)


class TestDepartmentService(unittest.TestCase):
    """Test cases for DepartmentService."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_department = MagicMock()
        self.mock_department.id = 1
        self.mock_department.name = 'Informática'

    @patch('app.services.department.DepartmentRepository')
    def test_create_success(self, mock_repo):
        """Test creating a department successfully."""
        from app.services import DepartmentService
        
        mock_repo.create.return_value = self.mock_department
        
        result = DepartmentService.create({'name': 'Informática'})
        
        self.assertEqual(result, self.mock_department)

    @patch('app.services.department.DepartmentRepository')
    def test_find_by_faculty(self, mock_repo):
        """Test finding departments by faculty."""
        from app.services import DepartmentService
        
        mock_repo.find_by_faculty.return_value = [self.mock_department]
        
        result = DepartmentService.find_by_faculty(1)
        
        self.assertEqual(len(result), 1)


class TestAreaService(unittest.TestCase):
    """Test cases for AreaService."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_area = MagicMock()
        self.mock_area.id = 1
        self.mock_area.name = 'Programación'

    @patch('app.services.area.AreaRepository')
    def test_create_success(self, mock_repo):
        """Test creating an area successfully."""
        from app.services import AreaService
        
        mock_repo.create.return_value = self.mock_area
        
        result = AreaService.create({'name': 'Programación'})
        
        self.assertEqual(result, self.mock_area)

    @patch('app.services.area.AreaRepository')
    def test_find_all(self, mock_repo):
        """Test finding all areas."""
        from app.services import AreaService
        
        mock_repo.find_all.return_value = [self.mock_area]
        
        result = AreaService.find_all()
        
        self.assertEqual(len(result), 1)


if __name__ == '__main__':
    unittest.main()
