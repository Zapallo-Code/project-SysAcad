"""Unit tests for FacultyViewSet."""

import unittest
from unittest.mock import patch, MagicMock
from rest_framework import status
from rest_framework.test import APIRequestFactory


class TestFacultyViewSet(unittest.TestCase):
    """Test cases for FacultyViewSet."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = APIRequestFactory()
        self.faculty_data = {"id": 1, "name": "Facultad de Ciencias Exactas"}
        self.mock_faculty = MagicMock()
        self.mock_faculty.id = 1

    @patch("app.views.faculty.FacultyService")
    @patch("app.views.faculty.FacultySerializer")
    def test_list_success(self, mock_serializer, mock_service):
        """Test listing faculties successfully."""
        from app.views import FacultyViewSet

        mock_service.find_all.return_value = [self.mock_faculty]
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.data = [self.faculty_data]
        mock_serializer.return_value = mock_serializer_instance

        viewset = FacultyViewSet()
        request = self.factory.get("/api/faculties/")
        response = viewset.list(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("app.views.faculty.FacultyService")
    @patch("app.views.faculty.FacultySerializer")
    def test_retrieve_success(self, mock_serializer, mock_service):
        """Test retrieving a faculty successfully."""
        from app.views import FacultyViewSet

        mock_service.find_by_id.return_value = self.mock_faculty
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.data = self.faculty_data
        mock_serializer.return_value = mock_serializer_instance

        viewset = FacultyViewSet()
        request = self.factory.get("/api/faculties/1/")
        response = viewset.retrieve(request, pk=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("app.views.faculty.FacultyService")
    def test_retrieve_not_found(self, mock_service):
        """Test retrieving a non-existent faculty."""
        from app.views import FacultyViewSet

        mock_service.find_by_id.return_value = None

        viewset = FacultyViewSet()
        request = self.factory.get("/api/faculties/999/")
        response = viewset.retrieve(request, pk=999)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


if __name__ == "__main__":
    unittest.main()
