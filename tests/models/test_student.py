"""Unit tests for Student model."""

import unittest
from unittest.mock import patch, MagicMock, PropertyMock
from datetime import date, timedelta
from django.core.exceptions import ValidationError


class TestStudentModel(unittest.TestCase):
    """Test cases for Student model."""

    def setUp(self):
        """Set up test fixtures."""
        # Create proper mock instances that behave like Django model instances
        self.mock_document_type = MagicMock(spec=['id', 'name', '_state'])
        self.mock_document_type.id = 1
        self.mock_document_type._state = MagicMock()

        self.mock_specialty = MagicMock(spec=['id', 'name', '_state'])
        self.mock_specialty.id = 1
        self.mock_specialty._state = MagicMock()

        self.valid_data = {
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

    @patch('app.models.student.Student.document_type', new_callable=PropertyMock)
    @patch('app.models.student.Student.specialty', new_callable=PropertyMock)
    def test_create_student_success(self, mock_specialty_prop, mock_doc_type_prop):
        """Test creating a student with valid data."""
        from app.models import Student

        mock_doc_type_prop.return_value = self.mock_document_type
        mock_specialty_prop.return_value = self.mock_specialty

        student = Student(**self.valid_data)
        self.assertEqual(student.first_name, "Juan")
        self.assertEqual(student.last_name, "Pérez")
        self.assertEqual(student.student_number, 12345)

    @patch('app.models.student.Student.document_type', new_callable=PropertyMock)
    @patch('app.models.student.Student.specialty', new_callable=PropertyMock)
    def test_full_name_property(self, mock_specialty_prop, mock_doc_type_prop):
        """Test full_name property returns correct format."""
        from app.models import Student

        mock_doc_type_prop.return_value = self.mock_document_type
        mock_specialty_prop.return_value = self.mock_specialty

        student = Student(**self.valid_data)
        expected = "Juan Pérez"
        self.assertEqual(student.full_name, expected)

    @patch('app.models.student.Student.document_type', new_callable=PropertyMock)
    @patch('app.models.student.Student.specialty', new_callable=PropertyMock)
    def test_str_representation(self, mock_specialty_prop, mock_doc_type_prop):
        """Test string representation of student."""
        from app.models import Student

        mock_doc_type_prop.return_value = self.mock_document_type
        mock_specialty_prop.return_value = self.mock_specialty

        student = Student(**self.valid_data)
        expected = "Pérez, Juan - Student Number: 12345"
        self.assertEqual(str(student), expected)

    @patch('app.models.student.Student.document_type', new_callable=PropertyMock)
    @patch('app.models.student.Student.specialty', new_callable=PropertyMock)
    def test_repr_representation(self, mock_specialty_prop, mock_doc_type_prop):
        """Test repr representation of student."""
        from app.models import Student

        mock_doc_type_prop.return_value = self.mock_document_type
        mock_specialty_prop.return_value = self.mock_specialty

        student = Student(**self.valid_data)
        expected = "<Student: Pérez, Juan>"
        self.assertEqual(repr(student), expected)

    @patch('app.models.student.Student.document_type', new_callable=PropertyMock)
    @patch('app.models.student.Student.specialty', new_callable=PropertyMock)
    def test_clean_birth_date_in_future(self, mock_specialty_prop, mock_doc_type_prop):
        """Test validation fails when birth date is in the future."""
        from app.models import Student

        mock_doc_type_prop.return_value = self.mock_document_type
        mock_specialty_prop.return_value = self.mock_specialty

        student = Student(
            **{**self.valid_data, "birth_date": date.today() + timedelta(days=1)}
        )

        with self.assertRaises(ValidationError) as context:
            student.clean()

        self.assertIn("birth_date", context.exception.message_dict)

    @patch('app.models.student.Student.document_type', new_callable=PropertyMock)
    @patch('app.models.student.Student.specialty', new_callable=PropertyMock)
    def test_clean_enrollment_before_birth(self, mock_specialty_prop, mock_doc_type_prop):
        """Test validation fails when enrollment date is before birth date."""
        from app.models import Student

        mock_doc_type_prop.return_value = self.mock_document_type
        mock_specialty_prop.return_value = self.mock_specialty

        student = Student(
            **{
                **self.valid_data,
                "birth_date": date(2000, 1, 1),
                "enrollment_date": date(1999, 12, 31),
            }
        )

        with self.assertRaises(ValidationError) as context:
            student.clean()

        self.assertIn("enrollment_date", context.exception.message_dict)

    @patch('app.models.student.Student.document_type', new_callable=PropertyMock)
    @patch('app.models.student.Student.specialty', new_callable=PropertyMock)
    def test_clean_valid_dates(self, mock_specialty_prop, mock_doc_type_prop):
        """Test validation passes with valid dates."""
        from app.models import Student

        mock_doc_type_prop.return_value = self.mock_document_type
        mock_specialty_prop.return_value = self.mock_specialty

        student = Student(**self.valid_data)

        try:
            student.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly!")

    @patch('app.models.student.Student.document_type', new_callable=PropertyMock)
    @patch('app.models.student.Student.specialty', new_callable=PropertyMock)
    def test_gender_choices(self, mock_specialty_prop, mock_doc_type_prop):
        """Test gender field accepts valid choices."""
        from app.models import Student

        mock_doc_type_prop.return_value = self.mock_document_type
        mock_specialty_prop.return_value = self.mock_specialty

        valid_genders = ["M", "F", "O"]
        for gender in valid_genders:
            student = Student(**{**self.valid_data, "gender": gender})
            self.assertEqual(student.gender, gender)

    def test_student_number_unique(self):
        """Test student_number field has unique constraint."""
        from app.models import Student

        field = Student._meta.get_field("student_number")
        self.assertTrue(field.unique)

    def test_meta_db_table(self):
        """Test that Meta.db_table is correctly set."""
        from app.models import Student

        self.assertEqual(Student._meta.db_table, "students")

    def test_meta_ordering(self):
        """Test that Meta.ordering is correctly set."""
        from app.models import Student

        self.assertEqual(Student._meta.ordering, ["last_name", "first_name"])

    def test_foreign_key_relationships(self):
        """Test foreign key relationships are properly defined."""
        from app.models import Student

        document_type_field = Student._meta.get_field("document_type")
        specialty_field = Student._meta.get_field("specialty")

        self.assertEqual(document_type_field.related_model.__name__, "DocumentType")
        self.assertEqual(specialty_field.related_model.__name__, "Specialty")


if __name__ == "__main__":
    unittest.main()
