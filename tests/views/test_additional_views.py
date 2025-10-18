"""Unit tests for SpecialtyViewSet, PlanViewSet, SubjectViewSet."""
import unittest
from unittest.mock import patch, MagicMock
from rest_framework import status
from rest_framework.test import APIRequestFactory


class TestSpecialtyViewSet(unittest.TestCase):
    """Test cases for SpecialtyViewSet."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = APIRequestFactory()
        self.specialty_data = {'id': 1, 'name': 'Computación'}
        self.mock_specialty = MagicMock()
        self.mock_specialty.id = 1

    @patch('app.views.specialty.SpecialtyService')
    @patch('app.views.specialty.SpecialtySerializer')
    def test_list_success(self, mock_serializer, mock_service):
        """Test listing specialties successfully."""
        from app.views import SpecialtyViewSet
        
        mock_service.find_all.return_value = [self.mock_specialty]
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.data = [self.specialty_data]
        mock_serializer.return_value = mock_serializer_instance
        
        viewset = SpecialtyViewSet()
        request = self.factory.get('/api/specialties/')
        response = viewset.list(request)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPlanViewSet(unittest.TestCase):
    """Test cases for PlanViewSet."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = APIRequestFactory()
        self.plan_data = {'id': 1, 'name': 'Plan 2020'}
        self.mock_plan = MagicMock()
        self.mock_plan.id = 1

    @patch('app.views.plan.PlanService')
    @patch('app.views.plan.PlanSerializer')
    def test_list_success(self, mock_serializer, mock_service):
        """Test listing plans successfully."""
        from app.views import PlanViewSet
        
        mock_service.find_all.return_value = [self.mock_plan]
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.data = [self.plan_data]
        mock_serializer.return_value = mock_serializer_instance
        
        viewset = PlanViewSet()
        request = self.factory.get('/api/plans/')
        response = viewset.list(request)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestSubjectViewSet(unittest.TestCase):
    """Test cases for SubjectViewSet."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = APIRequestFactory()
        self.subject_data = {'id': 1, 'name': 'AED', 'code': 'AED001'}
        self.mock_subject = MagicMock()
        self.mock_subject.id = 1

    @patch('app.views.subject.SubjectService')
    @patch('app.views.subject.SubjectSerializer')
    def test_list_success(self, mock_serializer, mock_service):
        """Test listing subjects successfully."""
        from app.views import SubjectViewSet
        
        mock_service.find_all.return_value = [self.mock_subject]
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.data = [self.subject_data]
        mock_serializer.return_value = mock_serializer_instance
        
        viewset = SubjectViewSet()
        request = self.factory.get('/api/subjects/')
        response = viewset.list(request)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('app.views.subject.SubjectService')
    @patch('app.views.subject.SubjectSerializer')
    def test_retrieve_success(self, mock_serializer, mock_service):
        """Test retrieving a subject successfully."""
        from app.views import SubjectViewSet
        
        mock_service.find_by_id.return_value = self.mock_subject
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.data = self.subject_data
        mock_serializer.return_value = mock_serializer_instance
        
        viewset = SubjectViewSet()
        request = self.factory.get('/api/subjects/1/')
        response = viewset.retrieve(request, pk=1)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


if __name__ == '__main__':
    unittest.main()
