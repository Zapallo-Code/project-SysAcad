"""Unit tests for generic ViewSets."""
import unittest
from unittest.mock import patch, MagicMock
from rest_framework import status
from rest_framework.test import APIRequestFactory


class GenericViewSetTestMixin:
    """Mixin for generic ViewSet tests."""
    
    viewset_class = None
    service_path = None
    serializer_path = None
    valid_data = None
    url_prefix = None
    
    def setUp(self):
        """Set up test fixtures."""
        self.factory = APIRequestFactory()
        self.mock_entity = MagicMock()
        self.mock_entity.id = 1
    
    def test_list_success(self):
        """Test listing entities successfully."""
        with patch(f'{self.service_path}') as mock_service, \
             patch(f'{self.serializer_path}') as mock_serializer:
            
            mock_service.find_all.return_value = [self.mock_entity]
            mock_serializer_instance = MagicMock()
            mock_serializer_instance.data = [self.valid_data]
            mock_serializer.return_value = mock_serializer_instance
            
            viewset = self.viewset_class()
            request = self.factory.get(f'{self.url_prefix}/')
            response = viewset.list(request)
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_success(self):
        """Test retrieving an entity successfully."""
        with patch(f'{self.service_path}') as mock_service, \
             patch(f'{self.serializer_path}') as mock_serializer:
            
            mock_service.find_by_id.return_value = self.mock_entity
            mock_serializer_instance = MagicMock()
            mock_serializer_instance.data = self.valid_data
            mock_serializer.return_value = mock_serializer_instance
            
            viewset = self.viewset_class()
            request = self.factory.get(f'{self.url_prefix}/1/')
            response = viewset.retrieve(request, pk=1)
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_not_found(self):
        """Test retrieving a non-existent entity."""
        with patch(f'{self.service_path}') as mock_service:
            mock_service.find_by_id.return_value = None
            
            viewset = self.viewset_class()
            request = self.factory.get(f'{self.url_prefix}/999/')
            response = viewset.retrieve(request, pk=999)
            
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_success(self):
        """Test creating an entity successfully."""
        with patch(f'{self.service_path}') as mock_service, \
             patch(f'{self.serializer_path}') as mock_serializer_class:
            
            mock_serializer = MagicMock()
            mock_serializer.is_valid.return_value = True
            mock_serializer.validated_data = self.valid_data
            mock_serializer.data = self.valid_data
            mock_serializer_class.return_value = mock_serializer
            
            mock_service.create.return_value = self.mock_entity
            
            viewset = self.viewset_class()
            request = self.factory.post(f'{self.url_prefix}/', self.valid_data)
            response = viewset.create(request)
            
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_invalid_data(self):
        """Test creating an entity with invalid data."""
        with patch(f'{self.serializer_path}') as mock_serializer_class:
            mock_serializer = MagicMock()
            mock_serializer.is_valid.return_value = False
            mock_serializer.errors = {'name': ['This field is required.']}
            mock_serializer_class.return_value = mock_serializer
            
            viewset = self.viewset_class()
            request = self.factory.post(f'{self.url_prefix}/', {})
            response = viewset.create(request)
            
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_destroy_success(self):
        """Test deleting an entity successfully."""
        with patch(f'{self.service_path}') as mock_service:
            mock_service.find_by_id.return_value = self.mock_entity
            mock_service.delete_by_id.return_value = True
            
            viewset = self.viewset_class()
            request = self.factory.delete(f'{self.url_prefix}/1/')
            response = viewset.destroy(request, pk=1)
            
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestDegreeViewSet(GenericViewSetTestMixin, unittest.TestCase):
    """Test cases for DegreeViewSet."""
    
    def setUp(self):
        """Set up test fixtures."""
        from app.views import DegreeViewSet
        super().setUp()
        self.viewset_class = DegreeViewSet
        self.service_path = 'app.views.degree.DegreeService'
        self.serializer_path = 'app.views.degree.DegreeSerializer'
        self.valid_data = {'id': 1, 'name': 'Ingeniería en Sistemas'}
        self.url_prefix = '/api/degrees'


class TestDocumentTypeViewSet(GenericViewSetTestMixin, unittest.TestCase):
    """Test cases for DocumentTypeViewSet."""
    
    def setUp(self):
        """Set up test fixtures."""
        from app.views import DocumentTypeViewSet
        super().setUp()
        self.viewset_class = DocumentTypeViewSet
        self.service_path = 'app.views.document_type.DocumentTypeService'
        self.serializer_path = 'app.views.document_type.DocumentTypeSerializer'
        self.valid_data = {'id': 1, 'name': 'DNI'}
        self.url_prefix = '/api/document-types'


class TestDepartmentViewSet(GenericViewSetTestMixin, unittest.TestCase):
    """Test cases for DepartmentViewSet."""
    
    def setUp(self):
        """Set up test fixtures."""
        from app.views import DepartmentViewSet
        super().setUp()
        self.viewset_class = DepartmentViewSet
        self.service_path = 'app.views.department.DepartmentService'
        self.serializer_path = 'app.views.department.DepartmentSerializer'
        self.valid_data = {'id': 1, 'name': 'Departamento de Computación'}
        self.url_prefix = '/api/departments'


class TestAreaViewSet(GenericViewSetTestMixin, unittest.TestCase):
    """Test cases for AreaViewSet."""
    
    def setUp(self):
        """Set up test fixtures."""
        from app.views import AreaViewSet
        super().setUp()
        self.viewset_class = AreaViewSet
        self.service_path = 'app.views.area.AreaService'
        self.serializer_path = 'app.views.area.AreaSerializer'
        self.valid_data = {'id': 1, 'name': 'Área de Sistemas'}
        self.url_prefix = '/api/areas'


if __name__ == '__main__':
    unittest.main()
