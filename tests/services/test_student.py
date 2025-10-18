"""Unit tests for StudentService."""

import unittest
from unittest.mock import patch, MagicMock
from datetime import date


class TestStudentService(unittest.TestCase):
    """Test cases for StudentService."""

    def setUp(self):
        """Set up test fixtures."""
        self.student_data = {
            "first_name": "Juan",
            "last_name": "Pérez",
            "document_number": "12345678",
            "birth_date": date(2000, 1, 1),
            "gender": "M",
            "student_number": 12345,
            "enrollment_date": date(2020, 3, 1),
            "document_type_id": 1,
            "specialty_id": 1,
        }

        self.mock_student = MagicMock()
        self.mock_student.id = 1
        self.mock_student.student_number = 12345

    @patch("app.services.student.StudentRepository")
    @patch("app.services.student.SpecialtyRepository")
    @patch("app.services.student.DocumentTypeRepository")
    @patch("app.services.student.transaction.atomic")
    def test_create_success(
        self, mock_atomic, mock_doc_type_repo, mock_specialty_repo, mock_repo
    ):
        """Test creating a student successfully."""
        from app.services import StudentService

        mock_specialty = MagicMock()
        mock_specialty.id = 1
        mock_specialty_repo.find_by_id.return_value = mock_specialty

        mock_doc_type = MagicMock()
        mock_doc_type.id = 1
        mock_doc_type_repo.find_by_id.return_value = mock_doc_type

        mock_repo.exists_by_student_number.return_value = False
        mock_repo.exists_by_document_number.return_value = False
        mock_repo.create.return_value = self.mock_student
        mock_atomic.return_value.__enter__ = MagicMock()
        mock_atomic.return_value.__exit__ = MagicMock()

        result = StudentService.create(self.student_data)

        mock_repo.create.assert_called_once_with(self.student_data)
        self.assertEqual(result, self.mock_student)

    @patch("app.services.student.StudentRepository")
    def test_create_duplicate_student_number(self, mock_repo):
        """Test creating a student with duplicate student number raises ValueError."""
        from app.services import StudentService

        mock_repo.exists_by_document_number.return_value = False
        mock_repo.exists_by_student_number.return_value = True

        with self.assertRaises(ValueError) as context:
            StudentService.create(self.student_data)

        self.assertIn("already taken", str(context.exception))

    @patch("app.services.student.StudentRepository")
    def test_find_by_id_success(self, mock_repo):
        """Test finding a student by ID successfully."""
        from app.services import StudentService

        mock_repo.find_by_id.return_value = self.mock_student

        result = StudentService.find_by_id(1)

        mock_repo.find_by_id.assert_called_once_with(1)
        self.assertEqual(result, self.mock_student)

    @patch("app.services.student.StudentRepository")
    def test_find_by_student_number(self, mock_repo):
        """Test finding a student by student number."""
        from app.services import StudentService

        mock_repo.find_by_student_number.return_value = self.mock_student

        result = StudentService.find_by_student_number(12345)

        mock_repo.find_by_student_number.assert_called_once_with(12345)
        self.assertEqual(result, self.mock_student)

    @patch("app.services.student.StudentRepository")
    def test_find_all(self, mock_repo):
        """Test finding all students."""
        from app.services import StudentService

        mock_students = [self.mock_student, MagicMock()]
        mock_repo.find_all.return_value = mock_students

        result = StudentService.find_all()

        mock_repo.find_all.assert_called_once()
        self.assertEqual(len(result), 2)

    @patch("app.services.student.StudentRepository")
    @patch("app.services.student.transaction.atomic")
    def test_update_success(self, mock_atomic, mock_repo):
        """Test updating a student successfully."""
        from app.services import StudentService

        existing = MagicMock()
        existing.id = 1
        existing.student_number = 12345

        mock_repo.find_by_id.return_value = existing
        mock_repo.update.return_value = self.mock_student
        mock_atomic.return_value.__enter__ = MagicMock()
        mock_atomic.return_value.__exit__ = MagicMock()

        update_data = {"first_name": "Carlos"}
        result = StudentService.update(1, update_data)

        mock_repo.update.assert_called_once()
        self.assertEqual(result, self.mock_student)

    @patch("app.services.student.StudentRepository")
    def test_update_not_found(self, mock_repo):
        """Test updating a non-existent student raises ValueError."""
        from app.services import StudentService

        mock_repo.find_by_id.return_value = None

        with self.assertRaises(ValueError) as context:
            StudentService.update(999, self.student_data)

        self.assertIn("does not exist", str(context.exception))

    @patch("app.services.student.StudentRepository")
    @patch("app.services.student.transaction.atomic")
    def test_delete_by_id_success(self, mock_atomic, mock_repo):
        """Test deleting a student successfully."""
        from app.services import StudentService

        mock_repo.exists_by_id.return_value = True
        mock_repo.delete_by_id.return_value = True
        mock_atomic.return_value.__enter__ = MagicMock()
        mock_atomic.return_value.__exit__ = MagicMock()

        result = StudentService.delete_by_id(1)

        mock_repo.delete_by_id.assert_called_once_with(1)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
