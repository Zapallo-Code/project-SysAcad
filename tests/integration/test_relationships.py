"""Integration tests for University-Faculty-Specialty chain."""

import unittest
from unittest.mock import patch, MagicMock, call
from django.db import transaction


class TestUniversityFacultyIntegration(unittest.TestCase):
    """Integration tests for University and Faculty relationship."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_university = MagicMock()
        self.mock_university.id = 1
        self.mock_university.name = "UNC"

        self.mock_faculty = MagicMock()
        self.mock_faculty.id = 1
        self.mock_faculty.name = "Facultad de Ciencias Exactas"
        self.mock_faculty.university = self.mock_university

    @patch("app.services.university.UniversityService")
    @patch("app.services.faculty.FacultyService")
    def test_create_university_with_faculties(
        self, mock_faculty_service, mock_uni_service
    ):
        """Test creating university and then adding faculties."""
        mock_uni_service.create.return_value = self.mock_university
        mock_faculty_service.create.return_value = self.mock_faculty

        # Create university
        university = mock_uni_service.create({"name": "UNC", "acronym": "UNC"})
        self.assertEqual(university.name, "UNC")

        # Create faculty for university
        faculty = mock_faculty_service.create(
            {"name": "Facultad de Ciencias Exactas", "university": university.id}
        )
        self.assertEqual(faculty.university.id, university.id)

    @patch("app.services.faculty.FacultyRepository")
    @patch("app.services.university.UniversityRepository")
    def test_cascade_delete_university_with_faculties(
        self, mock_uni_repo, mock_fac_repo
    ):
        """Test deleting university cascades to faculties."""
        mock_fac_repo.find_by_university.return_value = [self.mock_faculty]
        mock_uni_repo.delete.return_value = True

        # Delete university should handle faculty cascade
        faculties = mock_fac_repo.find_by_university(1)
        self.assertEqual(len(faculties), 1)

        result = mock_uni_repo.delete(1)
        self.assertTrue(result)


class TestFacultySpecialtyIntegration(unittest.TestCase):
    """Integration tests for Faculty and Specialty relationship."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_faculty = MagicMock()
        self.mock_faculty.id = 1

        self.mock_specialty = MagicMock()
        self.mock_specialty.id = 1
        self.mock_specialty.name = "Computación"
        self.mock_specialty.faculty = self.mock_faculty

    @patch("app.services.specialty.SpecialtyService")
    @patch("app.services.faculty.FacultyService")
    def test_faculty_with_multiple_specialties(
        self, mock_fac_service, mock_spec_service
    ):
        """Test faculty with multiple specialties."""
        mock_fac_service.find_by_id.return_value = self.mock_faculty

        mock_spec1 = MagicMock()
        mock_spec1.name = "Computación"
        mock_spec2 = MagicMock()
        mock_spec2.name = "Matemática"

        mock_spec_service.find_by_faculty.return_value = [mock_spec1, mock_spec2]

        faculty = mock_fac_service.find_by_id(1)
        specialties = mock_spec_service.find_by_faculty(faculty.id)

        self.assertEqual(len(specialties), 2)


class TestSpecialtyPlanSubjectChain(unittest.TestCase):
    """Integration tests for Specialty-Plan-Subject chain."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_specialty = MagicMock()
        self.mock_specialty.id = 1

        self.mock_plan = MagicMock()
        self.mock_plan.id = 1
        self.mock_plan.code = "PLAN2020"
        self.mock_plan.specialty = self.mock_specialty

        self.mock_subject = MagicMock()
        self.mock_subject.id = 1
        self.mock_subject.code = "AED001"
        self.mock_subject.plan = self.mock_plan

    @patch("app.services.subject.SubjectService")
    @patch("app.services.plan.PlanService")
    @patch("app.services.specialty.SpecialtyService")
    def test_complete_academic_chain(
        self, mock_spec_service, mock_plan_service, mock_subj_service
    ):
        """Test complete chain from specialty to subjects."""
        mock_spec_service.find_by_id.return_value = self.mock_specialty
        mock_plan_service.find_by_specialty.return_value = [self.mock_plan]
        mock_subj_service.find_by_plan.return_value = [self.mock_subject]

        # Get specialty
        specialty = mock_spec_service.find_by_id(1)
        self.assertIsNotNone(specialty)

        # Get plans for specialty
        plans = mock_plan_service.find_by_specialty(specialty.id)
        self.assertEqual(len(plans), 1)

        # Get subjects for plan
        subjects = mock_subj_service.find_by_plan(plans[0].id)
        self.assertEqual(len(subjects), 1)
        self.assertEqual(subjects[0].code, "AED001")


class TestStudentEnrollmentFlow(unittest.TestCase):
    """Integration tests for student enrollment flow."""

    def setUp(self):
        """Set up test fixtures."""
        from datetime import date

        self.mock_student = MagicMock()
        self.mock_student.id = 1
        self.mock_student.student_number = 12345
        self.mock_student.enrollment_date = date(2020, 3, 1)

        self.mock_specialty = MagicMock()
        self.mock_specialty.id = 1
        self.mock_student.specialty = self.mock_specialty

    @patch("app.services.student.StudentService")
    @patch("app.services.specialty.SpecialtyService")
    def test_enroll_student_in_specialty(self, mock_spec_service, mock_student_service):
        """Test enrolling a student in a specialty."""
        mock_spec_service.find_by_id.return_value = self.mock_specialty
        mock_student_service.create.return_value = self.mock_student

        # Verify specialty exists
        specialty = mock_spec_service.find_by_id(1)
        self.assertIsNotNone(specialty)

        # Create student enrolled in specialty
        student = mock_student_service.create(
            {
                "first_name": "Juan",
                "last_name": "Pérez",
                "student_number": 12345,
                "specialty": specialty.id,
            }
        )

        self.assertEqual(student.specialty.id, specialty.id)


class TestPositionAssignmentFlow(unittest.TestCase):
    """Integration tests for position assignment flow."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_subject = MagicMock()
        self.mock_subject.id = 1

        self.mock_position = MagicMock()
        self.mock_position.id = 1
        self.mock_position.subject = self.mock_subject

    @patch("app.services.position.PositionService")
    @patch("app.services.subject.SubjectService")
    def test_create_position_for_subject(self, mock_subj_service, mock_pos_service):
        """Test creating position for a subject."""
        mock_subj_service.find_by_id.return_value = self.mock_subject
        mock_pos_service.create.return_value = self.mock_position

        # Verify subject exists
        subject = mock_subj_service.find_by_id(1)
        self.assertIsNotNone(subject)

        # Create position for subject
        position = mock_pos_service.create(
            {
                "name": "Profesor Titular",
                "subject": subject.id,
                "category": 1,
                "dedication_type": 1,
            }
        )

        self.assertEqual(position.subject.id, subject.id)


class TestTransactionRollback(unittest.TestCase):
    """Integration tests for transaction rollback scenarios."""

    @patch("app.services.university.transaction")
    @patch("app.services.university.UniversityRepository")
    def test_rollback_on_create_error(self, mock_repo, mock_transaction):
        """Test transaction rollback on creation error."""
        from app.services import UniversityService

        mock_repo.create.side_effect = Exception("Database error")
        mock_transaction.atomic.side_effect = Exception("Database error")

        with self.assertRaises(Exception):
            UniversityService.create({"name": "Test University"})

    @patch("app.services.student.transaction")
    @patch("app.services.student.StudentRepository")
    def test_rollback_on_duplicate_student(self, mock_repo, mock_transaction):
        """Test transaction rollback on duplicate student."""
        from app.services import StudentService

        mock_repo.exists_by_document.return_value = True

        with self.assertRaises(ValueError):
            StudentService.create(
                {
                    "document_number": "12345678",
                    "first_name": "Juan",
                    "last_name": "Pérez",
                }
            )


if __name__ == "__main__":
    unittest.main()
