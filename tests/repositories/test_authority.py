"""Unit tests for AuthorityRepository."""

import unittest
from unittest.mock import patch, MagicMock
from django.core.exceptions import ObjectDoesNotExist


class TestAuthorityRepository(unittest.TestCase):
    """Test cases for AuthorityRepository."""

    def setUp(self):
        """Set up test fixtures."""
        self.authority_data = {
            "name": "Decano",
            "first_name": "Juan",
            "last_name": "Pérez",
            "faculty_id": 1,
        }

        self.mock_authority = MagicMock()
        self.mock_authority.id = 1
        self.mock_authority.name = "Decano"
        self.mock_authority.first_name = "Juan"
        self.mock_authority.last_name = "Pérez"

    @patch("app.repositories.authority.Authority")
    def test_create_success(self, mock_model):
        """Test creating an authority successfully."""
        from app.repositories import AuthorityRepository

        mock_instance = MagicMock()
        mock_model.return_value = mock_instance

        result = AuthorityRepository.create(self.authority_data)

        mock_instance.full_clean.assert_called_once()
        mock_instance.save.assert_called_once()

    @patch("app.repositories.authority.Authority.objects")
    def test_find_by_id_success(self, mock_objects):
        """Test finding an authority by ID."""
        from app.repositories import AuthorityRepository

        mock_select_related = MagicMock()
        mock_select_related.get.return_value = self.mock_authority
        mock_objects.select_related.return_value = mock_select_related

        result = AuthorityRepository.find_by_id(1)

        mock_objects.select_related.assert_called_once_with("position")
        mock_select_related.get.assert_called_once_with(id=1)
        self.assertEqual(result, self.mock_authority)

    @patch("app.repositories.authority.Authority.objects")
    def test_find_by_faculty(self, mock_objects):
        """Test finding authorities by faculty."""
        from app.repositories import AuthorityRepository

        mock_queryset = [self.mock_authority]
        mock_filter = MagicMock()
        mock_filter.select_related.return_value = mock_queryset
        mock_objects.filter.return_value = mock_filter

        result = AuthorityRepository.find_by_faculty(1)

        self.assertEqual(len(result), 1)

    @patch("app.repositories.authority.Authority.objects")
    def test_find_all(self, mock_objects):
        """Test finding all authorities."""
        from app.repositories import AuthorityRepository

        mock_queryset = [self.mock_authority, MagicMock()]
        mock_select_related = MagicMock()
        mock_select_related.all.return_value = mock_queryset
        mock_objects.select_related.return_value = mock_select_related

        result = AuthorityRepository.find_all()

        mock_objects.select_related.assert_called_once_with("position")
        mock_select_related.all.assert_called_once()
        self.assertEqual(len(result), 2)

    @patch("app.repositories.authority.Authority.objects")
    def test_search_by_name(self, mock_objects):
        """Test searching authorities by name."""
        from app.repositories import AuthorityRepository

        mock_queryset = [self.mock_authority]
        mock_objects.filter.return_value = mock_queryset

        result = AuthorityRepository.search_by_name("Juan")

        self.assertEqual(len(result), 1)


if __name__ == "__main__":
    unittest.main()
