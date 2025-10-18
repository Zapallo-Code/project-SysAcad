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

        mock_auth_list = [self.mock_authority]
        mock_queryset = MagicMock()
        mock_queryset.__iter__ = lambda x: iter(mock_auth_list)
        mock_queryset.select_related.return_value = mock_queryset
        mock_queryset.distinct.return_value = mock_auth_list

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

        mock_auth_list = [self.mock_authority]

        # Mock para el resultado final después de select_related
        mock_final_result = MagicMock()
        mock_final_result.__iter__ = lambda x: iter(mock_auth_list)

        # Mock para el segundo filter (last_name)
        mock_second_filter = MagicMock()
        mock_second_filter.select_related.return_value = mock_final_result

        # Mock para el primer filter (first_name) con soporte para operador |
        mock_first_filter = MagicMock()
        mock_first_filter.__or__ = lambda self, other: mock_final_result

        # Configurar objects.filter para retornar los mocks apropiados
        mock_objects.filter.side_effect = [mock_first_filter, mock_second_filter]

        result = AuthorityRepository.search_by_name("Juan")

        self.assertEqual(len(result), 1)


if __name__ == "__main__":
    unittest.main()
