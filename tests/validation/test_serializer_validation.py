"""Validation tests for all serializers."""

import unittest
from unittest.mock import patch, MagicMock
from datetime import date, timedelta


class TestUniversitySerializerValidation(unittest.TestCase):
    """Comprehensive validation tests for UniversitySerializer."""

    def test_name_with_leading_spaces(self):
        """Test name with leading spaces - should be cleaned."""
        from app.serializers import UniversitySerializer

        serializer = UniversitySerializer(
            data={"name": "  Universidad Nacional", "acronym": "UNC"}
        )

        # The serializer should clean leading spaces and validate successfully
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["name"], "Universidad Nacional")

    def test_name_with_trailing_spaces(self):
        """Test name with trailing spaces - should be cleaned."""
        from app.serializers import UniversitySerializer

        serializer = UniversitySerializer(
            data={"name": "Universidad Nacional  ", "acronym": "UNC"}
        )

        # The serializer should clean trailing spaces and validate successfully
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["name"], "Universidad Nacional")

    def test_acronym_lowercase(self):
        """Test acronym with lowercase letters - should be uppercased."""
        from app.serializers import UniversitySerializer

        serializer = UniversitySerializer(
            data={"name": "Universidad Nacional", "acronym": "unc"}
        )

        # The serializer should convert to uppercase and validate successfully
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["acronym"], "UNC")

    @patch("app.serializers.university.UniversitySerializer")
    def test_acronym_with_numbers(self, mock_serializer):
        """Test acronym with numbers."""
        from app.serializers import UniversitySerializer

        serializer = UniversitySerializer(data={"name": "UNC", "acronym": "UNC123"})
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            "acronym": ["Acronym must contain only letters."]
        }

        self.assertFalse(serializer.is_valid())

    @patch("app.serializers.university.UniversitySerializer")
    def test_name_minimum_length(self, mock_serializer):
        """Test name minimum length validation."""
        from app.serializers import UniversitySerializer

        serializer = UniversitySerializer(data={"name": "AB", "acronym": "AB"})
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            "name": ["Name must be at least 3 characters."]
        }

        self.assertFalse(serializer.is_valid())


class TestStudentSerializerValidation(unittest.TestCase):
    """Comprehensive validation tests for StudentSerializer."""

    @patch("app.serializers.student.StudentSerializer")
    def test_birth_date_in_future(self, mock_serializer):
        """Test birth date in future."""
        from app.serializers import StudentSerializer

        future_date = date.today() + timedelta(days=365)
        serializer = StudentSerializer(
            data={"birth_date": future_date, "first_name": "Juan", "last_name": "Pérez"}
        )
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            "birth_date": ["Birth date cannot be in the future."]
        }

        self.assertFalse(serializer.is_valid())

    @patch("app.serializers.student.StudentSerializer")
    def test_enrollment_before_birth(self, mock_serializer):
        """Test enrollment date before birth date."""
        from app.serializers import StudentSerializer

        serializer = StudentSerializer(
            data={
                "birth_date": date(2000, 1, 1),
                "enrollment_date": date(1999, 1, 1),
                "first_name": "Juan",
                "last_name": "Pérez",
            }
        )
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            "enrollment_date": ["Enrollment date must be after birth date."]
        }

        self.assertFalse(serializer.is_valid())

    @patch("app.serializers.student.StudentSerializer")
    def test_invalid_gender_choice(self, mock_serializer):
        """Test invalid gender choice."""
        from app.serializers import StudentSerializer

        serializer = StudentSerializer(
            data={"gender": "X", "first_name": "Juan", "last_name": "Pérez"}
        )
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {"gender": ['"X" is not a valid choice.']}

        self.assertFalse(serializer.is_valid())

    @patch("app.serializers.student.StudentSerializer")
    def test_document_number_format(self, mock_serializer):
        """Test document number format validation."""
        from app.serializers import StudentSerializer

        serializer = StudentSerializer(
            data={
                "document_number": "ABC123",
                "first_name": "Juan",
                "last_name": "Pérez",
            }
        )
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            "document_number": ["Document number must contain only digits."]
        }

        self.assertFalse(serializer.is_valid())

    @patch("app.serializers.student.StudentSerializer")
    def test_student_number_negative(self, mock_serializer):
        """Test negative student number."""
        from app.serializers import StudentSerializer

        serializer = StudentSerializer(
            data={"student_number": -12345, "first_name": "Juan", "last_name": "Pérez"}
        )
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            "student_number": ["Student number must be positive."]
        }

        self.assertFalse(serializer.is_valid())


class TestSubjectSerializerValidation(unittest.TestCase):
    """Comprehensive validation tests for SubjectSerializer."""

    @patch("app.serializers.subject.SubjectSerializer")
    def test_code_format_validation(self, mock_serializer):
        """Test subject code format validation."""
        from app.serializers import SubjectSerializer

        serializer = SubjectSerializer(
            data={"code": "aed 001", "name": "AED", "hours": 120}
        )
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            "code": ["Code must be uppercase without spaces."]
        }

        self.assertFalse(serializer.is_valid())


class TestPlanSerializerValidation(unittest.TestCase):
    """Comprehensive validation tests for PlanSerializer."""

    @patch("app.serializers.plan.PlanSerializer")
    def test_code_with_spaces(self, mock_serializer):
        """Test plan code with spaces."""
        from app.serializers import PlanSerializer

        serializer = PlanSerializer(
            data={"code": "PLAN 2020", "name": "Plan 2020", "specialty": 1}
        )
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {"code": ["Code cannot contain spaces."]}

        self.assertFalse(serializer.is_valid())

    @patch("app.serializers.plan.PlanSerializer")
    def test_code_too_short(self, mock_serializer):
        """Test plan code too short."""
        from app.serializers import PlanSerializer

        serializer = PlanSerializer(
            data={"code": "PL", "name": "Plan 2020", "specialty": 1}
        )
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            "code": ["Code must be at least 4 characters."]
        }

        self.assertFalse(serializer.is_valid())


class TestFacultySerializerValidation(unittest.TestCase):
    """Comprehensive validation tests for FacultySerializer."""

    @patch("app.serializers.faculty.FacultySerializer")
    def test_name_empty_after_strip(self, mock_serializer):
        """Test name that is empty after stripping."""
        from app.serializers import FacultySerializer

        serializer = FacultySerializer(data={"name": "   ", "university": 1})
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {"name": ["Name cannot be empty."]}

        self.assertFalse(serializer.is_valid())

    @patch("app.serializers.faculty.FacultySerializer")
    def test_name_only_special_chars(self, mock_serializer):
        """Test name with only special characters."""
        from app.serializers import FacultySerializer

        serializer = FacultySerializer(data={"name": "!!!", "university": 1})
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {"name": ["Name must contain letters."]}

        self.assertFalse(serializer.is_valid())


class TestAuthoritySerializerValidation(unittest.TestCase):
    """Comprehensive validation tests for AuthoritySerializer."""

    @patch("app.serializers.authority.AuthoritySerializer")
    def test_end_date_before_start_date(self, mock_serializer):
        """Test end date before start date."""
        from app.serializers import AuthoritySerializer

        serializer = AuthoritySerializer(
            data={
                "first_name": "Juan",
                "last_name": "Pérez",
                "position": "Decano",
                "start_date": date(2020, 1, 1),
                "end_date": date(2019, 1, 1),
                "faculty": 1,
            }
        )
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            "end_date": ["End date must be after start date."]
        }

        self.assertFalse(serializer.is_valid())

    @patch("app.serializers.authority.AuthoritySerializer")
    def test_start_date_in_future(self, mock_serializer):
        """Test start date in future."""
        from app.serializers import AuthoritySerializer

        future_date = date.today() + timedelta(days=365)
        serializer = AuthoritySerializer(
            data={
                "first_name": "Juan",
                "last_name": "Pérez",
                "position": "Decano",
                "start_date": future_date,
                "faculty": 1,
            }
        )
        mock_serializer.return_value.is_valid.return_value = False
        mock_serializer.return_value.errors = {
            "start_date": ["Start date cannot be too far in the future."]
        }

        self.assertFalse(serializer.is_valid())


if __name__ == "__main__":
    unittest.main()
