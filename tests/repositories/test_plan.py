"""Unit tests for PlanRepository."""

import unittest
from unittest.mock import patch, MagicMock
from django.core.exceptions import ObjectDoesNotExist


class TestPlanRepository(unittest.TestCase):
    """Test cases for PlanRepository."""

    def setUp(self):
        """Set up test fixtures."""
        self.plan_data = {"name": "Plan 2020", "code": "P2020", "specialty_id": 1}

        self.mock_plan = MagicMock()
        self.mock_plan.id = 1
        self.mock_plan.name = "Plan 2020"
        self.mock_plan.code = "P2020"

    @patch("app.repositories.plan.Plan")
    def test_create_success(self, mock_model):
        """Test creating a plan successfully."""
        from app.repositories import PlanRepository

        mock_instance = MagicMock()
        mock_model.return_value = mock_instance

        result = PlanRepository.create(self.plan_data)

        mock_instance.full_clean.assert_called_once()
        mock_instance.save.assert_called_once()

    @patch("app.repositories.plan.Plan.objects")
    def test_find_by_id_success(self, mock_objects):
        """Test finding a plan by ID."""
        from app.repositories import PlanRepository

        mock_objects.get.return_value = self.mock_plan

        result = PlanRepository.find_by_id(1)

        self.assertEqual(result, self.mock_plan)

    @patch("app.repositories.plan.Plan.objects")
    def test_find_by_code(self, mock_objects):
        """Test finding a plan by code."""
        from app.repositories import PlanRepository

        mock_objects.get.return_value = self.mock_plan

        result = PlanRepository.find_by_code("P2020")

        mock_objects.get.assert_called_once_with(code="P2020")

    @patch("app.repositories.plan.Plan.objects")
    def test_find_by_specialty(self, mock_objects):
        """Test finding plans by specialty."""
        from app.repositories import PlanRepository

        mock_queryset = [self.mock_plan]
        mock_objects.filter.return_value = mock_queryset

        result = PlanRepository.find_by_specialty(1)

        self.assertEqual(len(result), 1)

    @patch("app.repositories.plan.Plan.objects")
    def test_exists_by_code(self, mock_objects):
        """Test checking if plan exists by code."""
        from app.repositories import PlanRepository

        mock_filter = MagicMock()
        mock_filter.return_value.exists.return_value = True
        mock_objects.filter = mock_filter

        result = PlanRepository.exists_by_code("P2020")

        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
