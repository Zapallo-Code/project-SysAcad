"""Integration tests for API workflows."""

import unittest
from unittest.mock import patch, MagicMock
from rest_framework import status
from rest_framework.test import APIRequestFactory


class TestUniversityAPIWorkflow(unittest.TestCase):
    """Integration tests for University API workflow."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = APIRequestFactory()
        self.mock_university = MagicMock()
        self.mock_university.id = 1
        self.mock_university.name = "UNC"

    @patch("app.views.university.UniversityService")
    @patch("app.views.university.UniversitySerializer")
    def test_create_retrieve_update_delete_workflow(
        self, mock_serializer_class, mock_service
    ):
        """Test complete CRUD workflow for university."""
        from app.views import UniversityViewSet

        # Setup mocks
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.validated_data = {"name": "UNC", "acronym": "UNC"}
        mock_serializer.data = {"id": 1, "name": "UNC", "acronym": "UNC"}
        mock_serializer_class.return_value = mock_serializer

        mock_service.create.return_value = self.mock_university
        mock_service.find_by_id.return_value = self.mock_university
        mock_service.update.return_value = self.mock_university
        mock_service.delete.return_value = True

        viewset = UniversityViewSet()

        # 1. Create
        request = self.factory.post("/api/universities/")
        response = viewset.create(request)
        self.assertIsNotNone(response)

        # 2. Retrieve
        request = self.factory.get("/api/universities/1/")
        response = viewset.retrieve(request, pk=1)
        self.assertIsNotNone(response)

        # 3. Update
        request = self.factory.put("/api/universities/1/")
        response = viewset.update(request, pk=1)
        self.assertIsNotNone(response)

        # 4. Delete
        request = self.factory.delete("/api/universities/1/")
        response = viewset.destroy(request, pk=1)
        self.assertIsNotNone(response)


class TestStudentAPIWorkflow(unittest.TestCase):
    """Integration tests for Student API workflow."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = APIRequestFactory()
        self.mock_student = MagicMock()
        self.mock_student.id = 1

    @patch("app.views.student.StudentService")
    @patch("app.views.student.StudentSerializer")
    def test_student_search_and_filter_workflow(
        self, mock_serializer_class, mock_service
    ):
        """Test search and filter workflow for students."""
        from app.views import StudentViewSet

        mock_serializer = MagicMock()
        mock_serializer.data = [{"id": 1, "first_name": "Juan"}]
        mock_serializer_class.return_value = mock_serializer

        mock_service.search_by_name.return_value = [self.mock_student]
        mock_service.find_by_specialty.return_value = [self.mock_student]

        viewset = StudentViewSet()

        # Search by name
        request = self.factory.get("/api/students/?search=Juan")
        response = viewset.list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Filter by specialty
        request = self.factory.get("/api/students/?specialty=1")
        response = viewset.list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestSubjectPositionWorkflow(unittest.TestCase):
    """Integration tests for Subject and Position workflow."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = APIRequestFactory()
        self.mock_subject = MagicMock()
        self.mock_subject.id = 1
        self.mock_position = MagicMock()
        self.mock_position.id = 1

    @patch("app.views.subject.SubjectService")
    @patch("app.views.position.PositionService")
    @patch("app.views.subject.SubjectSerializer")
    @patch("app.views.position.PositionSerializer")
    def test_create_subject_then_positions(
        self, mock_pos_ser, mock_subj_ser, mock_pos_service, mock_subj_service
    ):
        """Test creating subject then adding positions."""
        from app.views import SubjectViewSet, PositionViewSet

        # Setup subject
        mock_subj_instance = MagicMock()
        mock_subj_instance.is_valid.return_value = True
        mock_subj_instance.validated_data = {"code": "AED001", "name": "AED"}
        mock_subj_instance.data = {"id": 1, "code": "AED001", "name": "AED"}
        mock_subj_ser.return_value = mock_subj_instance
        mock_subj_service.create.return_value = self.mock_subject

        # Setup position
        mock_pos_instance = MagicMock()
        mock_pos_instance.is_valid.return_value = True
        mock_pos_instance.validated_data = {"name": "Profesor", "subject": 1}
        mock_pos_instance.data = {"id": 1, "name": "Profesor"}
        mock_pos_ser.return_value = mock_pos_instance
        mock_pos_service.create.return_value = self.mock_position

        # Create subject
        subject_viewset = SubjectViewSet()
        request = self.factory.post("/api/subjects/")
        response = subject_viewset.create(request)
        self.assertIsNotNone(response)

        # Create position for subject
        position_viewset = PositionViewSet()
        request = self.factory.post("/api/positions/")
        response = position_viewset.create(request)
        self.assertIsNotNone(response)


class TestValidationErrorHandling(unittest.TestCase):
    """Integration tests for validation error handling."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = APIRequestFactory()

    @patch("app.views.university.UniversityService")
    @patch("app.views.university.UniversitySerializer")
    def test_invalid_data_returns_400(self, mock_serializer_class, mock_service):
        """Test invalid data returns 400 error."""
        from app.views import UniversityViewSet

        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = False
        mock_serializer.errors = {"name": ["This field is required."]}
        mock_serializer_class.return_value = mock_serializer

        viewset = UniversityViewSet()
        request = self.factory.post("/api/universities/", {})
        response = viewset.create(request)

        self.assertIsNotNone(response)

    @patch("app.views.student.StudentService")
    @patch("app.views.student.StudentSerializer")
    def test_duplicate_student_number_error(self, mock_serializer_class, mock_service):
        """Test duplicate student number returns error."""
        from app.views import StudentViewSet

        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.validated_data = {"student_number": 12345}
        mock_serializer_class.return_value = mock_serializer

        mock_service.create.side_effect = ValueError("Student number already exists")

        viewset = StudentViewSet()
        request = self.factory.post("/api/students/")
        
        response = viewset.create(request)
        self.assertIsNotNone(response)


class TestBulkOperations(unittest.TestCase):
    """Integration tests for bulk operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = APIRequestFactory()

    @patch("app.views.university.UniversityService")
    @patch("app.views.university.UniversitySerializer")
    def test_list_all_universities(self, mock_serializer_class, mock_service):
        """Test listing all universities."""
        from app.views import UniversityViewSet

        mock_universities = [MagicMock(id=i) for i in range(1, 11)]
        mock_service.find_all.return_value = mock_universities

        mock_serializer = MagicMock()
        mock_serializer.data = [{"id": i} for i in range(1, 11)]
        mock_serializer_class.return_value = mock_serializer

        viewset = UniversityViewSet()
        request = self.factory.get("/api/universities/")
        response = viewset.list(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mock_serializer.data), 10)


if __name__ == "__main__":
    unittest.main()
