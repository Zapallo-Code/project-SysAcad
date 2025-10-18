"""Unit tests for University model."""

import unittest
from unittest.mock import patch, MagicMock
from django.core.exceptions import ValidationError
from django.db import IntegrityError


class TestUniversityModel(unittest.TestCase):
    """Test cases for University model."""

    def setUp(self):
        """Set up test fixtures."""
        self.valid_data = {"name": "Universidad Nacional de Córdoba", "acronym": "UNC"}

    @patch("app.models.university.models.Model.save")
    @patch("app.models.university.University.full_clean")
    def test_create_university_success(self, mock_full_clean, mock_save):
        """Test creating a university with valid data."""
        from app.models import University

        university = University(**self.valid_data)
        university.save()

        mock_full_clean.assert_not_called()
        mock_save.assert_called_once()
        self.assertEqual(university.name, "Universidad Nacional de Córdoba")
        self.assertEqual(university.acronym, "UNC")

    def test_str_representation(self):
        """Test string representation of university."""
        from app.models import University

        university = University(**self.valid_data)
        expected = "UNC - Universidad Nacional de Córdoba"
        self.assertEqual(str(university), expected)

    def test_repr_representation(self):
        """Test repr representation of university."""
        from app.models import University

        university = University(**self.valid_data)
        expected = "<University: UNC>"
        self.assertEqual(repr(university), expected)

    def test_name_field_max_length(self):
        """Test name field respects max_length constraint."""
        from app.models import University

        university = University(name="A" * 100, acronym="TEST")
        self.assertEqual(len(university.name), 100)

    def test_acronym_field_max_length(self):
        """Test acronym field respects max_length constraint."""
        from app.models import University

        university = University(name="Test University", acronym="A" * 10)
        self.assertEqual(len(university.acronym), 10)

    def test_name_required(self):
        """Test that name is required."""
        from app.models import University

        university = University(acronym="TEST")
        with self.assertRaises((ValidationError, IntegrityError)):
            university.full_clean()

    def test_acronym_required(self):
        """Test that acronym is required."""
        from app.models import University

        university = University(name="Test University")
        with self.assertRaises((ValidationError, IntegrityError)):
            university.full_clean()

    def test_meta_db_table(self):
        """Test that Meta.db_table is correctly set."""
        from app.models import University

        self.assertEqual(University._meta.db_table, "universities")

    def test_meta_ordering(self):
        """Test that Meta.ordering is correctly set."""
        from app.models import University

        self.assertEqual(University._meta.ordering, ["name"])

    def test_meta_verbose_name(self):
        """Test that Meta.verbose_name is correctly set."""
        from app.models import University

        self.assertEqual(University._meta.verbose_name, "University")

    def test_meta_verbose_name_plural(self):
        """Test that Meta.verbose_name_plural is correctly set."""
        from app.models import University

        self.assertEqual(University._meta.verbose_name_plural, "Universities")


if __name__ == "__main__":
    unittest.main()
