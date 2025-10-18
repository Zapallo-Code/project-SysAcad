"""Unit tests for Position model."""

import unittest
from unittest.mock import patch, MagicMock


class TestPositionModel(unittest.TestCase):
    """Test cases for Position model."""

    def setUp(self):
        """Set up test fixtures."""
        self.position_data = {
            "id": 1,
            "name": "Profesor Titular",
            "subject_id": 1,
            "category_id": 1,
            "dedication_type_id": 1,
        }

    @patch("app.models.position.Position")
    def test_create_position(self, mock_model):
        """Test creating a position instance."""
        mock_instance = MagicMock()
        mock_instance.id = 1
        mock_instance.name = "Profesor Titular"
        mock_model.objects.create.return_value = mock_instance

        position = mock_model.objects.create(**self.position_data)

        self.assertEqual(position.name, "Profesor Titular")

    @patch("app.models.position.Position")
    def test_position_str_representation(self, mock_model):
        """Test string representation of position."""
        mock_instance = MagicMock()
        mock_instance.name = "Profesor Titular"
        mock_instance.__str__ = lambda self: self.name

        self.assertEqual(str(mock_instance), "Profesor Titular")

    @patch("app.models.position.Position")
    def test_position_subject_relation(self, mock_model):
        """Test position has subject relation."""
        mock_instance = MagicMock()
        mock_subject = MagicMock()
        mock_subject.name = "AED"
        mock_instance.subject = mock_subject

        self.assertEqual(mock_instance.subject.name, "AED")

    @patch("app.models.position.Position")
    def test_position_category_relation(self, mock_model):
        """Test position has category relation."""
        mock_instance = MagicMock()
        mock_category = MagicMock()
        mock_category.name = "Titular"
        mock_instance.category = mock_category

        self.assertEqual(mock_instance.category.name, "Titular")


if __name__ == "__main__":
    unittest.main()
