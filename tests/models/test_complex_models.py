"""Unit tests for complex models with relationships."""
import unittest
from unittest.mock import patch, MagicMock
from django.core.exceptions import ValidationError


class TestFacultyModel(unittest.TestCase):
    """Test cases for Faculty model."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_university = MagicMock()
        self.mock_university.id = 1
        
        self.valid_data = {
            'name': 'Facultad de Ciencias Exactas',
            'university': self.mock_university
        }

    def test_create_faculty_success(self):
        """Test creating a faculty with valid data."""
        from app.models import Faculty
        
        faculty = Faculty(**self.valid_data)
        self.assertEqual(faculty.name, 'Facultad de Ciencias Exactas')

    def test_faculty_university_relationship(self):
        """Test faculty has correct university relationship."""
        from app.models import Faculty
        
        faculty = Faculty(**self.valid_data)
        self.assertEqual(faculty.university, self.mock_university)


class TestSpecialtyModel(unittest.TestCase):
    """Test cases for Specialty model."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_faculty = MagicMock()
        self.mock_faculty.id = 1
        
        self.mock_specialty_type = MagicMock()
        self.mock_specialty_type.id = 1
        
        self.valid_data = {
            'name': 'Computación',
            'faculty': self.mock_faculty,
            'specialty_type': self.mock_specialty_type
        }

    def test_create_specialty_success(self):
        """Test creating a specialty with valid data."""
        from app.models import Specialty
        
        specialty = Specialty(**self.valid_data)
        self.assertEqual(specialty.name, 'Computación')

    def test_specialty_relationships(self):
        """Test specialty has correct relationships."""
        from app.models import Specialty
        
        specialty = Specialty(**self.valid_data)
        self.assertEqual(specialty.faculty, self.mock_faculty)
        self.assertEqual(specialty.specialty_type, self.mock_specialty_type)


class TestPlanModel(unittest.TestCase):
    """Test cases for Plan model."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_specialty = MagicMock()
        self.mock_specialty.id = 1
        
        self.valid_data = {
            'name': 'Plan 2020',
            'code': 'P2020',
            'specialty': self.mock_specialty
        }

    def test_create_plan_success(self):
        """Test creating a plan with valid data."""
        from app.models import Plan
        
        plan = Plan(**self.valid_data)
        self.assertEqual(plan.name, 'Plan 2020')
        self.assertEqual(plan.code, 'P2020')


class TestSubjectModel(unittest.TestCase):
    """Test cases for Subject model."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_plan = MagicMock()
        self.mock_plan.id = 1
        
        self.mock_area = MagicMock()
        self.mock_area.id = 1
        
        self.valid_data = {
            'name': 'Algoritmos y Estructuras de Datos',
            'code': 'AED',
            'plan': self.mock_plan,
            'area': self.mock_area
        }

    def test_create_subject_success(self):
        """Test creating a subject with valid data."""
        from app.models import Subject
        
        subject = Subject(**self.valid_data)
        self.assertEqual(subject.name, 'Algoritmos y Estructuras de Datos')
        self.assertEqual(subject.code, 'AED')


class TestPositionModel(unittest.TestCase):
    """Test cases for Position model."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_subject = MagicMock()
        self.mock_subject.id = 1
        
        self.mock_category = MagicMock()
        self.mock_category.id = 1
        
        self.mock_dedication = MagicMock()
        self.mock_dedication.id = 1
        
        self.valid_data = {
            'name': 'Profesor Titular',
            'subject': self.mock_subject,
            'position_category': self.mock_category,
            'dedication_type': self.mock_dedication
        }

    def test_create_position_success(self):
        """Test creating a position with valid data."""
        from app.models import Position
        
        position = Position(**self.valid_data)
        self.assertEqual(position.name, 'Profesor Titular')

    def test_position_relationships(self):
        """Test position has correct relationships."""
        from app.models import Position
        
        position = Position(**self.valid_data)
        self.assertEqual(position.subject, self.mock_subject)
        self.assertEqual(position.position_category, self.mock_category)
        self.assertEqual(position.dedication_type, self.mock_dedication)


class TestAuthorityModel(unittest.TestCase):
    """Test cases for Authority model."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_faculty = MagicMock()
        self.mock_faculty.id = 1
        
        self.valid_data = {
            'name': 'Decano',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'faculty': self.mock_faculty
        }

    def test_create_authority_success(self):
        """Test creating an authority with valid data."""
        from app.models import Authority
        
        authority = Authority(**self.valid_data)
        self.assertEqual(authority.name, 'Decano')
        self.assertEqual(authority.first_name, 'Juan')


class TestOrientationModel(unittest.TestCase):
    """Test cases for Orientation model."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_specialty = MagicMock()
        self.mock_specialty.id = 1
        
        self.valid_data = {
            'name': 'Orientación en Sistemas Distribuidos',
            'specialty': self.mock_specialty
        }

    def test_create_orientation_success(self):
        """Test creating an orientation with valid data."""
        from app.models import Orientation
        
        orientation = Orientation(**self.valid_data)
        self.assertEqual(orientation.name, 'Orientación en Sistemas Distribuidos')


class TestGroupModel(unittest.TestCase):
    """Test cases for Group model."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_subject = MagicMock()
        self.mock_subject.id = 1
        
        self.valid_data = {
            'name': 'Grupo A',
            'code': 'GA',
            'subject': self.mock_subject
        }

    def test_create_group_success(self):
        """Test creating a group with valid data."""
        from app.models import Group
        
        group = Group(**self.valid_data)
        self.assertEqual(group.name, 'Grupo A')
        self.assertEqual(group.code, 'GA')


if __name__ == '__main__':
    unittest.main()
