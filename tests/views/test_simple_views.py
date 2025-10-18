"""Unit tests for simple model ViewSets."""
import unittest
from unittest.mock import patch, MagicMock
from rest_framework import status
from rest_framework.test import APIRequestFactory


class TestDegreeViewSet(unittest.TestCase):
    """Test cases for DegreeViewSet."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = APIRequestFactory()
        self.degree_data = {'id': 1, 'name': 'Licenciatura'}
        self.mock_degree = MagicMock()
        self.mock_degree.id = 1

    @patch('app.views.degree.DegreeService')
    @patch('app.views.degree.DegreeSerializer')
    def test_list_success(self, mock_serializer, mock_service):
        """Test listing degrees successfully."""
        from app.views import DegreeViewSet
        
        mock_service.find_all.return_value = [self.mock_degree]
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.data = [self.degree_data]
        mock_serializer.return_value = mock_serializer_instance
        
        viewset = DegreeViewSet()
        request = self.factory.get('/api/degrees/')
        response = viewset.list(request)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDocumentTypeViewSet(unittest.TestCase):
    """Test cases for DocumentTypeViewSet."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = APIRequestFactory()
        self.doc_type_data = {'id': 1, 'name': 'DNI'}
        self.mock_doc_type = MagicMock()
        self.mock_doc_type.id = 1

    @patch('app.views.document_type.DocumentTypeService')
    @patch('app.views.document_type.DocumentTypeSerializer')
    def test_list_success(self, mock_serializer, mock_service):
        """Test listing document types successfully."""
        from app.views import DocumentTypeViewSet
        
        mock_service.find_all.return_value = [self.mock_doc_type]
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.data = [self.doc_type_data]
        mock_serializer.return_value = mock_serializer_instance
        
        viewset = DocumentTypeViewSet()
        request = self.factory.get('/api/document-types/')
        response = viewset.list(request)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDepartmentViewSet(unittest.TestCase):
    """Test cases for DepartmentViewSet."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = APIRequestFactory()
        self.department_data = {'id': 1, 'name': 'Departamento de Informática'}
        self.mock_department = MagicMock()
        self.mock_department.id = 1

    @patch('app.views.department.DepartmentService')
    @patch('app.views.department.DepartmentSerializer')
    def test_list_success(self, mock_serializer, mock_service):
        """Test listing departments successfully."""
        from app.views import DepartmentViewSet
        
        mock_service.find_all.return_value = [self.mock_department]
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.data = [self.department_data]
        mock_serializer.return_value = mock_serializer_instance
        
        viewset = DepartmentViewSet()
        request = self.factory.get('/api/departments/')
        response = viewset.list(request)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestAreaViewSet(unittest.TestCase):
    """Test cases for AreaViewSet."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = APIRequestFactory()
        self.area_data = {'id': 1, 'name': 'Programación'}
        self.mock_area = MagicMock()
        self.mock_area.id = 1

    @patch('app.views.area.AreaService')
    @patch('app.views.area.AreaSerializer')
    def test_list_success(self, mock_serializer, mock_service):
        """Test listing areas successfully."""
        from app.views import AreaViewSet
        
        mock_service.find_all.return_value = [self.mock_area]
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.data = [self.area_data]
        mock_serializer.return_value = mock_serializer_instance
        
        viewset = AreaViewSet()
        request = self.factory.get('/api/areas/')
        response = viewset.list(request)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('app.views.area.AreaService')
    @patch('app.views.area.AreaSerializer')
    def test_retrieve_success(self, mock_serializer, mock_service):
        """Test retrieving an area successfully."""
        from app.views import AreaViewSet
        
        mock_service.find_by_id.return_value = self.mock_area
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.data = self.area_data
        mock_serializer.return_value = mock_serializer_instance
        
        viewset = AreaViewSet()
        request = self.factory.get('/api/areas/1/')
        response = viewset.retrieve(request, pk=1)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


if __name__ == '__main__':
    unittest.main()
