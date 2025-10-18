"""Unit tests for StudentViewSet."""
import unittest
from unittest.mock import patch, MagicMock
from rest_framework import status
from rest_framework.test import APIRequestFactory


class TestStudentViewSet(unittest.TestCase):
    """Test cases for StudentViewSet."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = APIRequestFactory()
        self.student_data = {
            'id': 1,
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'student_number': 12345
        }
        
        self.mock_student = MagicMock()
        self.mock_student.id = 1

    @patch('app.views.student.StudentService')
    @patch('app.views.student.StudentSerializer')
    def test_list_students_success(self, mock_serializer, mock_service):
        """Test listing students successfully."""
        from app.views import StudentViewSet
        
        mock_service.find_all.return_value = [self.mock_student]
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.data = [self.student_data]
        mock_serializer.return_value = mock_serializer_instance
        
        viewset = StudentViewSet()
        request = self.factory.get('/api/students/')
        response = viewset.list(request)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('app.views.student.StudentService')
    @patch('app.views.student.StudentSerializer')
    def test_retrieve_student_success(self, mock_serializer, mock_service):
        """Test retrieving a student successfully."""
        from app.views import StudentViewSet
        
        mock_service.find_by_id.return_value = self.mock_student
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.data = self.student_data
        mock_serializer.return_value = mock_serializer_instance
        
        viewset = StudentViewSet()
        request = self.factory.get('/api/students/1/')
        response = viewset.retrieve(request, pk=1)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('app.views.student.StudentService')
    def test_retrieve_student_not_found(self, mock_service):
        """Test retrieving a non-existent student."""
        from app.views import StudentViewSet
        
        mock_service.find_by_id.return_value = None
        
        viewset = StudentViewSet()
        request = self.factory.get('/api/students/999/')
        response = viewset.retrieve(request, pk=999)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('app.views.student.StudentService')
    @patch('app.views.student.StudentSerializer')
    def test_create_student_success(self, mock_serializer_class, mock_service):
        """Test creating a student successfully."""
        from app.views import StudentViewSet
        
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.validated_data = self.student_data
        mock_serializer.data = self.student_data
        mock_serializer_class.return_value = mock_serializer
        
        mock_service.create.return_value = self.mock_student
        
        viewset = StudentViewSet()
        request = self.factory.post('/api/students/', self.student_data)
        response = viewset.create(request)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('app.views.student.StudentSerializer')
    def test_create_student_invalid_data(self, mock_serializer_class):
        """Test creating a student with invalid data."""
        from app.views import StudentViewSet
        
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = False
        mock_serializer.errors = {'first_name': ['This field is required.']}
        mock_serializer_class.return_value = mock_serializer
        
        viewset = StudentViewSet()
        request = self.factory.post('/api/students/', {})
        response = viewset.create(request)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


if __name__ == '__main__':
    unittest.main()
