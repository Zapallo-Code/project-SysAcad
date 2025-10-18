"""Error handling tests for services."""

import unittest
from unittest.mock import patch, MagicMock
from django.db import IntegrityError, DatabaseError


class TestUniversityServiceErrors(unittest.TestCase):
    """Error handling tests for UniversityService."""

    @patch("app.services.university.UniversityRepository")
    def test_create_duplicate_name_error(self, mock_repo):
        """Test creating university with duplicate name."""
        from app.services import UniversityService

        mock_repo.exists_by_name.return_value = True

        with self.assertRaises(ValueError) as context:
            UniversityService.create({"name": "UNC", "acronym": "UNC"})

        self.assertIn("already taken", str(context.exception))

    @patch("app.services.university.UniversityRepository")
    def test_create_database_error(self, mock_repo):
        """Test database error during creation."""
        from app.services import UniversityService

        mock_repo.create.side_effect = DatabaseError("Connection lost")

        with self.assertRaises(DatabaseError):
            UniversityService.create({"name": "Test", "acronym": "TST"})

    @patch("app.services.university.UniversityRepository")
    def test_update_not_found_error(self, mock_repo):
        """Test updating non-existent university."""
        from app.services import UniversityService

        mock_repo.find_by_id.return_value = None

        with self.assertRaises(ValueError) as context:
            UniversityService.update(999, {"name": "Updated"})

        self.assertIn("does not exist", str(context.exception))


class TestStudentServiceErrors(unittest.TestCase):
    """Error handling tests for StudentService."""

    @patch("app.services.student.StudentRepository")
    def test_create_duplicate_document_error(self, mock_repo):
        """Test creating student with duplicate document."""
        from app.services import StudentService

        mock_repo.exists_by_document_number.return_value = True

        with self.assertRaises(ValueError) as context:
            StudentService.create(
                {
                    "document_number": "12345678",
                    "first_name": "Juan",
                    "last_name": "Pérez",
                }
            )

        self.assertIn("already taken", str(context.exception).lower())

    @patch("app.services.student.StudentRepository")
    def test_create_duplicate_student_number_error(self, mock_repo):
        """Test creating student with duplicate student number."""
        from app.services import StudentService

        mock_repo.exists_by_document_number.return_value = False
        mock_repo.exists_by_student_number.return_value = True

        with self.assertRaises(ValueError) as context:
            StudentService.create(
                {
                    "document_number": "12345678",
                    "student_number": 12345,
                    "first_name": "Juan",
                    "last_name": "Pérez",
                }
            )

        self.assertIn("already taken", str(context.exception).lower())

    @patch("app.services.student.StudentRepository")
    def test_invalid_specialty_error(self, mock_repo):
        """Test creating student with invalid specialty."""
        from app.services import StudentService

        mock_repo.exists_by_document.return_value = False
        mock_repo.create.side_effect = IntegrityError("Foreign key constraint")

        with self.assertRaises(IntegrityError):
            StudentService.create(
                {
                    "document_number": "12345678",
                    "first_name": "Juan",
                    "last_name": "Pérez",
                    "specialty": 9999,
                }
            )


class TestSubjectServiceErrors(unittest.TestCase):
    """Error handling tests for SubjectService."""

    @patch("app.services.subject.SubjectRepository")
    def test_create_duplicate_code_error(self, mock_repo):
        """Test creating subject with duplicate code."""
        from app.services import SubjectService

        mock_repo.exists_by_code.return_value = True

        with self.assertRaises(ValueError) as context:
            SubjectService.create({"code": "AED001", "name": "AED", "hours": 120})

        self.assertIn("code", str(context.exception).lower())

    @patch("app.services.subject.SubjectRepository")
    def test_invalid_plan_error(self, mock_repo):
        """Test creating subject with invalid plan."""
        from app.services import SubjectService

        mock_repo.exists_by_code.return_value = False
        mock_repo.create.side_effect = IntegrityError("Invalid plan reference")

        with self.assertRaises(IntegrityError):
            SubjectService.create(
                {"code": "AED001", "name": "AED", "hours": 120, "plan": 9999}
            )


class TestPlanServiceErrors(unittest.TestCase):
    """Error handling tests for PlanService."""

    @patch("app.services.plan.PlanRepository")
    def test_create_duplicate_code_error(self, mock_repo):
        """Test creating plan with duplicate code."""
        from app.services import PlanService

        mock_repo.exists_by_name.return_value = True

        with self.assertRaises(ValueError) as context:
            PlanService.create(
                {"code": "PLAN2020", "name": "Plan 2020", "specialty": 1}
            )

        self.assertIn("already taken", str(context.exception).lower())


class TestFacultyServiceErrors(unittest.TestCase):
    """Error handling tests for FacultyService."""

    @patch("app.services.faculty.FacultyRepository")
    def test_create_with_invalid_university(self, mock_repo):
        """Test creating faculty with invalid university."""
        from app.services import FacultyService

        mock_repo.create.side_effect = IntegrityError("Invalid university")

        with self.assertRaises(IntegrityError):
            FacultyService.create({"name": "Test Faculty", "university": 9999})


class TestRepositoryErrors(unittest.TestCase):
    """Error handling tests for repository operations."""

    @patch("app.repositories.university.University")
    def test_get_object_does_not_exist(self, mock_model):
        """Test get when object does not exist."""
        from app.repositories import UniversityRepository
        from django.core.exceptions import ObjectDoesNotExist

        mock_model.objects.get.side_effect = ObjectDoesNotExist()

        result = UniversityRepository.find_by_id(999)

        self.assertIsNone(result)

    @patch("app.repositories.student.Student")
    def test_multiple_objects_returned(self, mock_model):
        """Test when multiple objects are returned."""
        from app.repositories import StudentRepository
        from django.core.exceptions import MultipleObjectsReturned

        mock_select_related = MagicMock()
        mock_select_related.get.side_effect = MultipleObjectsReturned()
        mock_model.objects.select_related.return_value = mock_select_related

        # find_by_student_number catches MultipleObjectsReturned and returns None
        result = StudentRepository.find_by_student_number(12345)
        self.assertIsNone(result)

    @patch("app.repositories.subject.Subject")
    def test_database_connection_error(self, mock_model):
        """Test database connection error."""
        from app.repositories import SubjectRepository

        mock_model.objects.all.side_effect = DatabaseError("Connection failed")

        with self.assertRaises(DatabaseError):
            SubjectRepository.find_all()


class TestTransactionErrors(unittest.TestCase):
    """Error handling tests for transactions."""

    @patch("app.services.university.UniversityRepository")
    def test_transaction_atomic_rollback(self, mock_repo):
        """Test transaction rollback on error."""
        from app.services import UniversityService

        # Simulate repository error
        mock_repo.create.side_effect = DatabaseError("Error during creation")
        mock_repo.exists_by_name.return_value = False
        mock_repo.exists_by_acronym.return_value = False

        with self.assertRaises(DatabaseError):
            UniversityService.create({"name": "Test", "acronym": "TST"})


if __name__ == "__main__":
    unittest.main()
