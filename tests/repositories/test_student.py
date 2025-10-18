"""Unit tests for StudentRepository."""

import unittest
from unittest.mock import patch, MagicMock
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from datetime import date


class TestStudentRepository(unittest.TestCase):
    """Test cases for StudentRepository."""

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
        self.mock_student.first_name = "Juan"
        self.mock_student.last_name = "Pérez"
        self.mock_student.student_number = 12345

    @patch("app.repositories.student.Student")
    def test_create_success(self, mock_student_model):
        """Test creating a student successfully."""
        from app.repositories import StudentRepository

        mock_instance = MagicMock()
        mock_student_model.return_value = mock_instance

        result = StudentRepository.create(self.student_data)

        mock_student_model.assert_called_once_with(**self.student_data)
        mock_instance.full_clean.assert_called_once()
        mock_instance.save.assert_called_once()

    @patch("app.repositories.student.Student.objects")
    def test_find_by_id_success(self, mock_objects):
        """Test finding a student by ID successfully."""
        from app.repositories import StudentRepository

        mock_select_related = MagicMock()
        mock_select_related.get.return_value = self.mock_student
        mock_objects.select_related.return_value = mock_select_related

        result = StudentRepository.find_by_id(1)

        mock_objects.select_related.assert_called_once_with(
            "document_type", "specialty"
        )
        mock_select_related.get.assert_called_once_with(id=1)
        self.assertEqual(result, self.mock_student)

    @patch("app.repositories.student.Student.objects")
    def test_find_by_student_number(self, mock_objects):
        """Test finding a student by student number."""
        from app.repositories import StudentRepository

        mock_select_related = MagicMock()
        mock_select_related.get.return_value = self.mock_student
        mock_objects.select_related.return_value = mock_select_related

        result = StudentRepository.find_by_student_number(12345)

        mock_objects.select_related.assert_called_once_with(
            "document_type", "specialty"
        )
        mock_select_related.get.assert_called_once_with(student_number=12345)
        self.assertEqual(result, self.mock_student)

    @patch("app.repositories.student.Student.objects")
    def test_find_by_document_number(self, mock_objects):
        """Test finding a student by document number."""
        from app.repositories import StudentRepository

        mock_filter = MagicMock()
        mock_filter.select_related.return_value = [self.mock_student]
        mock_objects.filter.return_value = mock_filter

        result = StudentRepository.find_by_document_number("12345678")

        mock_objects.filter.assert_called_once_with(document_number="12345678")
        mock_filter.select_related.assert_called_once_with("document_type", "specialty")

    @patch("app.repositories.student.Student.objects")
    def test_find_all(self, mock_objects):
        """Test finding all students."""
        from app.repositories import StudentRepository

        mock_queryset = [self.mock_student, MagicMock()]
        mock_select_related = MagicMock()
        mock_select_related.all.return_value = mock_queryset
        mock_objects.select_related.return_value = mock_select_related

        result = StudentRepository.find_all()

        mock_objects.select_related.assert_called_once_with(
            "document_type", "specialty"
        )
        mock_select_related.all.assert_called_once()
        self.assertEqual(len(result), 2)

    @patch("app.repositories.student.Student.objects")
    def test_search_by_name(self, mock_objects):
        """Test searching students by name."""
        from app.repositories import StudentRepository

        mock_queryset = [self.mock_student]
        mock_filter = MagicMock()
        mock_filter.return_value = mock_queryset
        mock_objects.filter = mock_filter

        result = StudentRepository.search_by_name("Juan")

        self.assertEqual(len(result), 1)

    @patch("app.repositories.student.Student")
    def test_update_success(self, mock_student_model):
        """Test updating a student successfully."""
        from app.repositories import StudentRepository

        result = StudentRepository.update(self.mock_student)

        self.mock_student.full_clean.assert_called_once()
        self.mock_student.save.assert_called_once()

    @patch("app.repositories.student.StudentRepository.find_by_id")
    def test_delete_by_id_success(self, mock_find):
        """Test deleting a student by ID successfully."""
        from app.repositories import StudentRepository

        mock_find.return_value = self.mock_student

        result = StudentRepository.delete_by_id(1)

        mock_find.assert_called_once_with(1)
        self.mock_student.delete.assert_called_once()
        self.assertTrue(result)

    @patch("app.repositories.student.Student.objects")
    def test_exists_by_student_number(self, mock_objects):
        """Test checking if student exists by student number."""
        from app.repositories import StudentRepository

        mock_filter = MagicMock()
        mock_filter.return_value.exists.return_value = True
        mock_objects.filter = mock_filter

        result = StudentRepository.exists_by_student_number(12345)

        self.assertTrue(result)

    @patch("app.repositories.student.Student.objects")
    def test_count(self, mock_objects):
        """Test counting students."""
        from app.repositories import StudentRepository

        mock_objects.count.return_value = 10

        result = StudentRepository.count()

        self.assertEqual(result, 10)


if __name__ == "__main__":
    unittest.main()
