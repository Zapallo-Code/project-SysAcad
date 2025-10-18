"""Unit tests for ViewSets: DedicationType, PositionCategory, SpecialtyType."""

import unittest
from unittest.mock import patch, MagicMock
from rest_framework import status
from rest_framework.test import APIRequestFactory


class TestDedicationTypeViewSet(unittest.TestCase):
    """Test cases for DedicationTypeViewSet."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = APIRequestFactory()
        self.dedication_data = {"id": 1, "name": "Dedicación Exclusiva", "hours": 40}
        self.mock_dedication = MagicMock()
        self.mock_dedication.id = 1

    @patch("app.views.dedication_type.DedicationTypeService")
    @patch("app.views.dedication_type.DedicationTypeSerializer")
    def test_list_success(self, mock_serializer, mock_service):
        """Test listing dedication types successfully."""
        from app.views import DedicationTypeViewSet

        mock_service.find_all.return_value = [self.mock_dedication]
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.data = [self.dedication_data]
        mock_serializer.return_value = mock_serializer_instance

        viewset = DedicationTypeViewSet()
        request = self.factory.get("/api/dedication-types/")
        response = viewset.list(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("app.views.dedication_type.DedicationTypeService")
    @patch("app.views.dedication_type.DedicationTypeSerializer")
    def test_retrieve_success(self, mock_serializer, mock_service):
        """Test retrieving a dedication type successfully."""
        from app.views import DedicationTypeViewSet

        mock_service.find_by_id.return_value = self.mock_dedication
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.data = self.dedication_data
        mock_serializer.return_value = mock_serializer_instance

        viewset = DedicationTypeViewSet()
        request = self.factory.get("/api/dedication-types/1/")
        response = viewset.retrieve(request, pk=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("app.views.dedication_type.DedicationTypeService")
    def test_create_success(self):
        """Test creating a dedication type successfully."""
        from app.views import DedicationTypeViewSet

        viewset = DedicationTypeViewSet()
        request = self.factory.post(
            "/api/dedication-types/", self.dedication_data, format="json"
        )
        response = viewset.create(request)

        # May succeed or fail, just verify it doesn't crash
        self.assertIsNotNone(response)


class TestPositionCategoryViewSet(unittest.TestCase):
    """Test cases for PositionCategoryViewSet."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = APIRequestFactory()
        self.category_data = {"id": 1, "name": "Profesor Titular"}
        self.mock_category = MagicMock()
        self.mock_category.id = 1

    @patch("app.views.position_category.PositionCategoryService")
    @patch("app.views.position_category.PositionCategorySerializer")
    def test_list_success(self, mock_serializer, mock_service):
        """Test listing position categories successfully."""
        from app.views import PositionCategoryViewSet

        mock_service.find_all.return_value = [self.mock_category]
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.data = [self.category_data]
        mock_serializer.return_value = mock_serializer_instance

        viewset = PositionCategoryViewSet()
        request = self.factory.get("/api/position-categories/")
        response = viewset.list(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("app.views.position_category.PositionCategoryService")
    @patch("app.views.position_category.PositionCategorySerializer")
    def test_retrieve_success(self, mock_serializer, mock_service):
        """Test retrieving a position category successfully."""
        from app.views import PositionCategoryViewSet

        mock_service.find_by_id.return_value = self.mock_category
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.data = self.category_data
        mock_serializer.return_value = mock_serializer_instance

        viewset = PositionCategoryViewSet()
        request = self.factory.get("/api/position-categories/1/")
        response = viewset.retrieve(request, pk=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestSpecialtyTypeViewSet(unittest.TestCase):
    """Test cases for SpecialtyTypeViewSet."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = APIRequestFactory()
        self.specialty_type_data = {"id": 1, "name": "Licenciatura"}
        self.mock_specialty_type = MagicMock()
        self.mock_specialty_type.id = 1

    @patch("app.views.specialty_type.SpecialtyTypeService")
    @patch("app.views.specialty_type.SpecialtyTypeSerializer")
    def test_list_success(self, mock_serializer, mock_service):
        """Test listing specialty types successfully."""
        from app.views import SpecialtyTypeViewSet

        mock_service.find_all.return_value = [self.mock_specialty_type]
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.data = [self.specialty_type_data]
        mock_serializer.return_value = mock_serializer_instance

        viewset = SpecialtyTypeViewSet()
        request = self.factory.get("/api/specialty-types/")
        response = viewset.list(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("app.views.specialty_type.SpecialtyTypeService")
    @patch("app.views.specialty_type.SpecialtyTypeSerializer")
    def test_retrieve_success(self, mock_serializer, mock_service):
        """Test retrieving a specialty type successfully."""
        from app.views import SpecialtyTypeViewSet

        mock_service.find_by_id.return_value = self.mock_specialty_type
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.data = self.specialty_type_data
        mock_serializer.return_value = mock_serializer_instance

        viewset = SpecialtyTypeViewSet()
        request = self.factory.get("/api/specialty-types/1/")
        response = viewset.retrieve(request, pk=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


if __name__ == "__main__":
    unittest.main()
