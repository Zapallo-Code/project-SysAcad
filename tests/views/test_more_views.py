"""Unit tests for ViewSets: Position, Authority, Orientation, Group."""

import unittest
from unittest.mock import patch, MagicMock
from rest_framework import status
from rest_framework.test import APIRequestFactory


class TestPositionViewSet(unittest.TestCase):
    """Test cases for PositionViewSet."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = APIRequestFactory()
        self.position_data = {"id": 1, "name": "Profesor Titular"}
        self.mock_position = MagicMock()
        self.mock_position.id = 1

    @patch("app.views.position.PositionService")
    @patch("app.views.position.PositionSerializer")
    def test_list_success(self, mock_serializer, mock_service):
        """Test listing positions successfully."""
        from app.views import PositionViewSet

        mock_service.find_all.return_value = [self.mock_position]
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.data = [self.position_data]
        mock_serializer.return_value = mock_serializer_instance

        viewset = PositionViewSet()
        request = self.factory.get("/api/positions/")
        response = viewset.list(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("app.views.position.PositionService")
    @patch("app.views.position.PositionSerializer")
    def test_retrieve_success(self, mock_serializer, mock_service):
        """Test retrieving a position successfully."""
        from app.views import PositionViewSet

        mock_service.find_by_id.return_value = self.mock_position
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.data = self.position_data
        mock_serializer.return_value = mock_serializer_instance

        viewset = PositionViewSet()
        request = self.factory.get("/api/positions/1/")
        response = viewset.retrieve(request, pk=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestAuthorityViewSet(unittest.TestCase):
    """Test cases for AuthorityViewSet."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = APIRequestFactory()
        self.authority_data = {"id": 1, "first_name": "Juan", "last_name": "Pérez"}
        self.mock_authority = MagicMock()
        self.mock_authority.id = 1

    @patch("app.views.authority.AuthorityService")
    @patch("app.views.authority.AuthoritySerializer")
    def test_list_success(self, mock_serializer, mock_service):
        """Test listing authorities successfully."""
        from app.views import AuthorityViewSet

        mock_service.find_all.return_value = [self.mock_authority]
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.data = [self.authority_data]
        mock_serializer.return_value = mock_serializer_instance

        viewset = AuthorityViewSet()
        request = self.factory.get("/api/authorities/")
        response = viewset.list(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestOrientationViewSet(unittest.TestCase):
    """Test cases for OrientationViewSet."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = APIRequestFactory()
        self.orientation_data = {"id": 1, "name": "Sistemas de Información"}
        self.mock_orientation = MagicMock()
        self.mock_orientation.id = 1

    @patch("app.views.orientation.OrientationService")
    @patch("app.views.orientation.OrientationSerializer")
    def test_list_success(self, mock_serializer, mock_service):
        """Test listing orientations successfully."""
        from app.views import OrientationViewSet

        mock_service.find_all.return_value = [self.mock_orientation]
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.data = [self.orientation_data]
        mock_serializer.return_value = mock_serializer_instance

        viewset = OrientationViewSet()
        request = self.factory.get("/api/orientations/")
        response = viewset.list(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestGroupViewSet(unittest.TestCase):
    """Test cases for GroupViewSet."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = APIRequestFactory()
        self.group_data = {"id": 1, "name": "Grupo A", "code": "GA001"}
        self.mock_group = MagicMock()
        self.mock_group.id = 1

    @patch("app.views.group.GroupService")
    @patch("app.views.group.GroupSerializer")
    def test_list_success(self, mock_serializer, mock_service):
        """Test listing groups successfully."""
        from app.views import GroupViewSet

        mock_service.find_all.return_value = [self.mock_group]
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.data = [self.group_data]
        mock_serializer.return_value = mock_serializer_instance

        viewset = GroupViewSet()
        request = self.factory.get("/api/groups/")
        response = viewset.list(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("app.views.group.GroupService")
    @patch("app.views.group.GroupSerializer")
    def test_retrieve_success(self, mock_serializer, mock_service):
        """Test retrieving a group successfully."""
        from app.views import GroupViewSet

        mock_service.find_by_id.return_value = self.mock_group
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.data = self.group_data
        mock_serializer.return_value = mock_serializer_instance

        viewset = GroupViewSet()
        request = self.factory.get("/api/groups/1/")
        response = viewset.retrieve(request, pk=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


if __name__ == "__main__":
    unittest.main()
