"""Unit tests for OrientationRepository."""

import unittest
from unittest.mock import patch, MagicMock
from django.core.exceptions import ObjectDoesNotExist


class TestOrientationRepository(unittest.TestCase):
    """Test cases for OrientationRepository."""

    def setUp(self):
        """Set up test fixtures."""
        self.orientation_data = {"name": "Sistemas Distribuidos", "specialty_id": 1}

        self.mock_orientation = MagicMock()
        self.mock_orientation.id = 1
        self.mock_orientation.name = "Sistemas Distribuidos"

    @patch("app.repositories.orientation.Orientation")
    def test_create_success(self, mock_model):
        """Test creating an orientation successfully."""
        from app.repositories import OrientationRepository

        mock_instance = MagicMock()
        mock_model.return_value = mock_instance

        result = OrientationRepository.create(self.orientation_data)

        mock_instance.full_clean.assert_called_once()
        mock_instance.save.assert_called_once()

    @patch("app.repositories.orientation.Orientation.objects")
    def test_find_by_id_success(self, mock_objects):
        """Test finding an orientation by ID."""
        from app.repositories import OrientationRepository

        mock_select_related = MagicMock()
        mock_select_related.get.return_value = self.mock_orientation
        mock_objects.select_related.return_value = mock_select_related

        result = OrientationRepository.find_by_id(1)

        mock_objects.select_related.assert_called_once_with(
            "specialty", "plan", "subject"
        )
        mock_select_related.get.assert_called_once_with(id=1)
        self.assertEqual(result, self.mock_orientation)

    @patch("app.repositories.orientation.Orientation.objects")
    def test_find_by_specialty(self, mock_objects):
        """Test finding orientations by specialty."""
        from app.repositories import OrientationRepository

        mock_queryset = [self.mock_orientation]
        mock_filter = MagicMock()
        mock_filter.select_related.return_value = mock_queryset
        mock_objects.filter.return_value = mock_filter

        result = OrientationRepository.find_by_specialty(1)

        self.assertEqual(len(result), 1)

    @patch("app.repositories.orientation.Orientation.objects")
    def test_find_all(self, mock_objects):
        """Test finding all orientations."""
        from app.repositories import OrientationRepository

        mock_queryset = [self.mock_orientation, MagicMock()]
        mock_select_related = MagicMock()
        mock_select_related.all.return_value = mock_queryset
        mock_objects.select_related.return_value = mock_select_related

        result = OrientationRepository.find_all()

        mock_objects.select_related.assert_called_once_with(
            "specialty", "plan", "subject"
        )
        mock_select_related.all.assert_called_once()
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()
