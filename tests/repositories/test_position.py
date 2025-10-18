"""Unit tests for PositionRepository."""

import unittest
from unittest.mock import patch, MagicMock
from django.core.exceptions import ObjectDoesNotExist


class TestPositionRepository(unittest.TestCase):
    """Test cases for PositionRepository."""

    def setUp(self):
        """Set up test fixtures."""
        self.position_data = {
            "name": "Profesor Titular",
            "subject_id": 1,
            "position_category_id": 1,
            "dedication_type_id": 1,
        }

        self.mock_position = MagicMock()
        self.mock_position.id = 1
        self.mock_position.name = "Profesor Titular"

    @patch("app.repositories.position.Position")
    def test_create_success(self, mock_model):
        """Test creating a position successfully."""
        from app.repositories import PositionRepository

        mock_instance = MagicMock()
        mock_model.return_value = mock_instance

        result = PositionRepository.create(self.position_data)

        mock_instance.full_clean.assert_called_once()
        mock_instance.save.assert_called_once()

    @patch("app.repositories.position.Position.objects")
    def test_find_by_id_success(self, mock_objects):
        """Test finding a position by ID."""
        from app.repositories import PositionRepository

        mock_select_related = MagicMock()
        mock_select_related.get.return_value = self.mock_position
        mock_objects.select_related.return_value = mock_select_related

        result = PositionRepository.find_by_id(1)

        mock_objects.select_related.assert_called_once_with(
            "position_category", "dedication_type"
        )
        mock_select_related.get.assert_called_once_with(id=1)
        self.assertEqual(result, self.mock_position)

    @patch("app.repositories.position.Position.objects")
    def test_find_by_subject(self, mock_objects):
        """Test finding positions by subject."""
        from app.repositories import PositionRepository

        mock_pos_list = [self.mock_position]
        mock_queryset = MagicMock()
        mock_queryset.__iter__ = lambda x: iter(mock_pos_list)
        mock_queryset.select_related.return_value = mock_queryset
        mock_queryset.distinct.return_value = mock_pos_list

        mock_filter = MagicMock()
        mock_filter.select_related.return_value = mock_queryset
        mock_objects.filter.return_value = mock_filter

        result = PositionRepository.find_by_subject(1)

        self.assertEqual(len(result), 1)

    @patch("app.repositories.position.Position.objects")
    def test_find_by_category(self, mock_objects):
        """Test finding positions by category."""
        from app.repositories import PositionRepository

        mock_queryset = [self.mock_position]
        mock_filter = MagicMock()
        mock_filter.select_related.return_value = mock_queryset
        mock_objects.filter.return_value = mock_filter

        result = PositionRepository.find_by_category(1)

        self.assertEqual(len(result), 1)

    @patch("app.repositories.position.Position.objects")
    def test_find_all(self, mock_objects):
        """Test finding all positions."""
        from app.repositories import PositionRepository

        mock_queryset = [self.mock_position, MagicMock()]
        mock_select_related = MagicMock()
        mock_select_related.all.return_value = mock_queryset
        mock_objects.select_related.return_value = mock_select_related

        result = PositionRepository.find_all()

        mock_objects.select_related.assert_called_once_with(
            "position_category", "dedication_type"
        )
        mock_select_related.all.assert_called_once()
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()
