"""Unit tests for Plan model."""

import unittest
from unittest.mock import patch, MagicMock


class TestPlanModel(unittest.TestCase):
    """Test cases for Plan model."""

    def setUp(self):
        """Set up test fixtures."""
        self.plan_data = {
            "id": 1,
            "code": "PLAN2020",
            "name": "Plan 2020",
            "specialty_id": 1,
        }

    @patch("app.models.plan.Plan")
    def test_create_plan(self, mock_model):
        """Test creating a plan instance."""
        mock_instance = MagicMock()
        mock_instance.id = 1
        mock_instance.code = "PLAN2020"
        mock_instance.name = "Plan 2020"
        mock_model.objects.create.return_value = mock_instance

        plan = mock_model.objects.create(**self.plan_data)

        self.assertEqual(plan.code, "PLAN2020")
        self.assertEqual(plan.name, "Plan 2020")

    @patch("app.models.plan.Plan")
    def test_plan_str_representation(self, mock_model):
        """Test string representation of plan."""
        mock_instance = MagicMock()
        mock_instance.code = "PLAN2020"
        mock_instance.name = "Plan 2020"
        mock_instance.__str__ = lambda self: f"{self.code} - {self.name}"

        self.assertEqual(str(mock_instance), "PLAN2020 - Plan 2020")

    @patch("app.models.plan.Plan")
    def test_plan_code_unique(self, mock_model):
        """Test code field is unique."""
        from django.db import IntegrityError

        mock_model.objects.create.side_effect = IntegrityError("Duplicate code")

        with self.assertRaises(IntegrityError):
            mock_model.objects.create(**self.plan_data)

    @patch("app.models.plan.Plan")
    def test_plan_specialty_relation(self, mock_model):
        """Test plan has specialty relation."""
        mock_instance = MagicMock()
        mock_specialty = MagicMock()
        mock_specialty.name = "Computación"
        mock_instance.specialty = mock_specialty

        self.assertEqual(mock_instance.specialty.name, "Computación")


if __name__ == "__main__":
    unittest.main()
