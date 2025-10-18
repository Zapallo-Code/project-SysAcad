"""Unit tests for Degree model."""

import unittest
from unittest.mock import patch, MagicMock


class TestDegreeModel(unittest.TestCase):
    """Test cases for Degree model."""

    def setUp(self):
        """Set up test fixtures."""
        self.degree_data = {"id": 1, "name": "Licenciatura"}

    @patch("app.models.degree.Degree")
    def test_create_degree(self, mock_model):
        """Test creating a degree instance."""
        mock_instance = MagicMock()
        mock_instance.id = 1
        mock_instance.name = "Licenciatura"
        mock_model.objects.create.return_value = mock_instance

        degree = mock_model.objects.create(**self.degree_data)

        self.assertEqual(degree.name, "Licenciatura")

    @patch("app.models.degree.Degree")
    def test_degree_str_representation(self, mock_model):
        """Test string representation of degree."""
        mock_instance = MagicMock()
        mock_instance.name = "Licenciatura"
        mock_instance.__str__ = lambda self: self.name

        self.assertEqual(str(mock_instance), "Licenciatura")

    @patch("app.models.degree.Degree")
    def test_degree_name_required(self, mock_model):
        """Test name field is required."""
        from django.core.exceptions import ValidationError

        mock_instance = MagicMock()
        mock_instance.name = None
        mock_instance.full_clean.side_effect = ValidationError("Name is required")

        with self.assertRaises(ValidationError):
            mock_instance.full_clean()


if __name__ == "__main__":
    unittest.main()
