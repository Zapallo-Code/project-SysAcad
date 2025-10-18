"""Unit tests for PlanService, SubjectService, PositionService, AuthorityService, OrientationService."""

import unittest
from unittest.mock import patch, MagicMock


class TestPlanService(unittest.TestCase):
    """Test cases for PlanService."""

    def setUp(self):
        """Set up test fixtures."""
        self.plan_data = {"name": "Plan 2020", "code": "P2020", "specialty_id": 1}
        self.mock_plan = MagicMock()
        self.mock_plan.id = 1

    @patch("app.services.plan.PlanRepository")
    def test_create_success(self, mock_repo):
        """Test creating a plan successfully."""
        from app.services import PlanService

        mock_repo.exists_by_name.return_value = False
        mock_repo.create.return_value = self.mock_plan
        result = PlanService.create(self.plan_data)
        self.assertEqual(result, self.mock_plan)

    @patch("app.services.plan.PlanRepository")
    def test_find_by_id(self, mock_repo):
        """Test finding a plan by ID."""
        from app.services import PlanService

        mock_repo.find_by_id.return_value = self.mock_plan
        result = PlanService.find_by_id(1)
        self.assertEqual(result, self.mock_plan)


class TestSubjectService(unittest.TestCase):
    """Test cases for SubjectService."""

    def setUp(self):
        """Set up test fixtures."""
        self.subject_data = {"name": "AED", "code": "AED001", "plan_id": 1}
        self.mock_subject = MagicMock()
        self.mock_subject.id = 1

    @patch("app.services.subject.SubjectRepository")
    def test_create_success(self, mock_repo):
        """Test creating a subject successfully."""
        from app.services import SubjectService

        mock_repo.exists_by_code.return_value = False
        mock_repo.create.return_value = self.mock_subject
        result = SubjectService.create(self.subject_data)
        self.assertEqual(result, self.mock_subject)

    @patch("app.services.subject.SubjectRepository")
    def test_find_by_code(self, mock_repo):
        """Test finding a subject by code."""
        from app.services import SubjectService

        mock_repo.find_by_code.return_value = self.mock_subject
        result = SubjectService.find_by_code("AED001")
        self.assertEqual(result, self.mock_subject)


class TestPositionService(unittest.TestCase):
    """Test cases for PositionService."""

    def setUp(self):
        """Set up test fixtures."""
        self.position_data = {"name": "Profesor", "subject_id": 1}
        self.mock_position = MagicMock()
        self.mock_position.id = 1

    @patch("app.services.position.PositionRepository")
    def test_create_success(self, mock_repo):
        """Test creating a position successfully."""
        from app.services import PositionService

        mock_repo.exists_by_name.return_value = False
        mock_repo.create.return_value = self.mock_position
        result = PositionService.create(self.position_data)
        self.assertEqual(result, self.mock_position)


class TestAuthorityService(unittest.TestCase):
    """Test cases for AuthorityService."""

    def setUp(self):
        """Set up test fixtures."""
        self.authority_data = {
            "name": "Decano",
            "first_name": "Juan",
            "last_name": "Pérez",
        }
        self.mock_authority = MagicMock()
        self.mock_authority.id = 1

    @patch("app.services.authority.AuthorityRepository")
    def test_create_success(self, mock_repo):
        """Test creating an authority successfully."""
        from app.services import AuthorityService

        mock_repo.create.return_value = self.mock_authority
        result = AuthorityService.create(self.authority_data)
        self.assertEqual(result, self.mock_authority)


class TestOrientationService(unittest.TestCase):
    """Test cases for OrientationService."""

    def setUp(self):
        """Set up test fixtures."""
        self.orientation_data = {"name": "Sistemas Distribuidos", "specialty_id": 1}
        self.mock_orientation = MagicMock()
        self.mock_orientation.id = 1

    @patch("app.services.orientation.OrientationRepository")
    @patch("app.services.orientation.SpecialtyRepository")
    def test_create_success(self, mock_specialty_repo, mock_repo):
        """Test creating an orientation successfully."""
        from app.services import OrientationService

        mock_repo.exists_by_name.return_value = False
        mock_specialty_repo.exists_by_id.return_value = True
        mock_repo.create.return_value = self.mock_orientation
        result = OrientationService.create(self.orientation_data)
        self.assertEqual(result, self.mock_orientation)


if __name__ == "__main__":
    unittest.main()
