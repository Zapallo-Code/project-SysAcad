"""Unit tests for simple model repositories: Degree, DocumentType, Department, Area."""

import unittest
from unittest.mock import patch, MagicMock


class TestDegreeRepository(unittest.TestCase):
    """Test cases for DegreeRepository."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_degree = MagicMock()
        self.mock_degree.id = 1
        self.mock_degree.name = "Licenciatura"

    @patch("app.repositories.degree.Degree")
    def test_create_success(self, mock_model):
        """Test creating a degree successfully."""
        from app.repositories import DegreeRepository

        mock_instance = self.mock_degree
        mock_model.return_value = mock_instance

        result = DegreeRepository.create({"name": "Licenciatura"})

        mock_model.assert_called_once_with(name="Licenciatura")
        mock_instance.full_clean.assert_called_once()
        mock_instance.save.assert_called_once()
        self.assertEqual(result, self.mock_degree)

    @patch("app.repositories.degree.Degree")
    def test_find_by_id_success(self, mock_model):
        """Test finding a degree by ID successfully."""
        from app.repositories import DegreeRepository

        mock_model.objects.get.return_value = self.mock_degree

        result = DegreeRepository.find_by_id(1)

        self.assertEqual(result, self.mock_degree)

    @patch("app.repositories.degree.Degree")
    def test_find_all(self, mock_model):
        """Test finding all degrees."""
        from app.repositories import DegreeRepository

        mock_model.objects.all.return_value = [self.mock_degree]

        result = DegreeRepository.find_all()

        self.assertEqual(len(result), 1)


class TestDocumentTypeRepository(unittest.TestCase):
    """Test cases for DocumentTypeRepository."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_doc_type = MagicMock()
        self.mock_doc_type.id = 1
        self.mock_doc_type.name = "DNI"

    @patch("app.repositories.document_type.DocumentType")
    def test_create_success(self, mock_model):
        """Test creating a document type successfully."""
        from app.repositories import DocumentTypeRepository

        mock_instance = self.mock_doc_type
        mock_model.return_value = mock_instance

        result = DocumentTypeRepository.create({"name": "DNI"})

        mock_model.assert_called_once_with(name="DNI")
        mock_instance.full_clean.assert_called_once()
        mock_instance.save.assert_called_once()
        self.assertEqual(result, self.mock_doc_type)

    @patch("app.repositories.document_type.DocumentType")
    def test_find_by_name(self, mock_model):
        """Test finding document type by name."""
        from app.repositories import DocumentTypeRepository

        mock_model.objects.get.return_value = self.mock_doc_type

        result = DocumentTypeRepository.find_by_name("DNI")

        self.assertEqual(result, self.mock_doc_type)


class TestDepartmentRepository(unittest.TestCase):
    """Test cases for DepartmentRepository."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_department = MagicMock()
        self.mock_department.id = 1
        self.mock_department.name = "Informática"

    @patch("app.repositories.department.Department")
    def test_create_success(self, mock_model):
        """Test creating a department successfully."""
        from app.repositories import DepartmentRepository

        mock_instance = self.mock_department
        mock_model.return_value = mock_instance

        result = DepartmentRepository.create({"name": "Informática", "faculty": 1})

        mock_model.assert_called_once_with(name="Informática", faculty=1)
        mock_instance.full_clean.assert_called_once()
        mock_instance.save.assert_called_once()
        self.assertEqual(result, self.mock_department)

    @patch("app.repositories.department.Department")
    def test_find_by_faculty(self, mock_model):
        """Test finding departments by faculty."""
        from app.repositories import DepartmentRepository

        mock_dept_list = [self.mock_department]
        mock_queryset = MagicMock()
        mock_queryset.__iter__ = lambda x: iter(mock_dept_list)
        mock_queryset.select_related.return_value = mock_dept_list
        mock_model.objects.filter.return_value = mock_queryset

        result = DepartmentRepository.find_by_faculty(1)

        self.assertEqual(len(result), 1)


class TestAreaRepository(unittest.TestCase):
    """Test cases for AreaRepository."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_area = MagicMock()
        self.mock_area.id = 1
        self.mock_area.name = "Programación"

    @patch("app.repositories.area.Area")
    def test_create_success(self, mock_model):
        """Test creating an area successfully."""
        from app.repositories import AreaRepository

        mock_instance = self.mock_area
        mock_model.return_value = mock_instance

        result = AreaRepository.create({"name": "Programación"})

        mock_model.assert_called_once_with(name="Programación")
        mock_instance.full_clean.assert_called_once()
        mock_instance.save.assert_called_once()
        self.assertEqual(result, self.mock_area)

    @patch("app.repositories.area.Area")
    def test_find_by_id(self, mock_model):
        """Test finding area by ID."""
        from app.repositories import AreaRepository

        mock_model.objects.get.return_value = self.mock_area

        result = AreaRepository.find_by_id(1)

        self.assertEqual(result, self.mock_area)

    @patch("app.repositories.area.Area")
    def test_find_all(self, mock_model):
        """Test finding all areas."""
        from app.repositories import AreaRepository

        mock_model.objects.all.return_value = [self.mock_area]

        result = AreaRepository.find_all()

        self.assertEqual(len(result), 1)


if __name__ == "__main__":
    unittest.main()
