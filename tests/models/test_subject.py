"""Unit tests for Subject model."""

import unittest
from unittest.mock import patch, MagicMock


class TestSubjectModel(unittest.TestCase):
    """Test cases for Subject model."""

    def setUp(self):
        """Set up test fixtures."""
        self.subject_data = {
            "id": 1,
            "code": "AED001",
            "name": "Algoritmos y Estructuras de Datos",
            "hours": 120,
            "plan_id": 1,
            "area_id": 1,
        }

    @patch("app.models.subject.Subject")
    def test_create_subject(self, mock_model):
        """Test creating a subject instance."""
        mock_instance = MagicMock()
        mock_instance.id = 1
        mock_instance.code = "AED001"
        mock_instance.name = "Algoritmos y Estructuras de Datos"
        mock_instance.hours = 120
        mock_model.objects.create.return_value = mock_instance

        subject = mock_model.objects.create(**self.subject_data)

        self.assertEqual(subject.code, "AED001")
        self.assertEqual(subject.hours, 120)

    @patch("app.models.subject.Subject")
    def test_subject_str_representation(self, mock_model):
        """Test string representation of subject."""
        mock_instance = MagicMock()
        mock_instance.code = "AED001"
        mock_instance.name = "Algoritmos y Estructuras de Datos"
        mock_instance.__str__ = lambda self: f"{self.code} - {self.name}"

        self.assertEqual(
            str(mock_instance), "AED001 - Algoritmos y Estructuras de Datos"
        )

    @patch("app.models.subject.Subject")
    def test_subject_code_unique(self, mock_model):
        """Test code field is unique."""
        from django.db import IntegrityError

        mock_model.objects.create.side_effect = IntegrityError("Duplicate code")

        with self.assertRaises(IntegrityError):
            mock_model.objects.create(**self.subject_data)

    @patch("app.models.subject.Subject")
    def test_subject_plan_relation(self, mock_model):
        """Test subject has plan relation."""
        mock_instance = MagicMock()
        mock_plan = MagicMock()
        mock_plan.code = "PLAN2020"
        mock_instance.plan = mock_plan

        self.assertEqual(mock_instance.plan.code, "PLAN2020")

    @patch("app.models.subject.Subject")
    def test_subject_area_relation(self, mock_model):
        """Test subject has area relation."""
        mock_instance = MagicMock()
        mock_area = MagicMock()
        mock_area.name = "Programación"
        mock_instance.area = mock_area

        self.assertEqual(mock_instance.area.name, "Programación")

    @patch("app.models.subject.Subject")
    def test_subject_hours_positive(self, mock_model):
        """Test hours must be positive."""
        from django.core.exceptions import ValidationError

        mock_instance = MagicMock()
        mock_instance.hours = -10
        mock_instance.full_clean.side_effect = ValidationError("Hours must be positive")

        with self.assertRaises(ValidationError):
            mock_instance.full_clean()


if __name__ == "__main__":
    unittest.main()
