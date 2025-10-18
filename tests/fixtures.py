"""Common test fixtures and utilities."""
import unittest
from unittest.mock import MagicMock
from datetime import date


class BaseTestCase(unittest.TestCase):
    """Base test case with common utilities."""
    
    def assertDictContainsSubset(self, subset, dictionary, msg=None):
        """Check that dictionary contains all items in subset."""
        for key, value in subset.items():
            if key not in dictionary:
                self.fail(f"Key '{key}' not found in dictionary")
            if dictionary[key] != value:
                self.fail(f"Value mismatch for key '{key}': {dictionary[key]} != {value}")


class ModelFactory:
    """Factory for creating mock model instances."""
    
    @staticmethod
    def create_university(id=1, name='Test University', acronym='TU'):
        """Create a mock University instance."""
        mock = MagicMock()
        mock.id = id
        mock.name = name
        mock.acronym = acronym
        return mock
    
    @staticmethod
    def create_student(id=1, first_name='Juan', last_name='Pérez', 
                      student_number=12345, document_number='12345678'):
        """Create a mock Student instance."""
        mock = MagicMock()
        mock.id = id
        mock.first_name = first_name
        mock.last_name = last_name
        mock.student_number = student_number
        mock.document_number = document_number
        mock.birth_date = date(2000, 1, 1)
        mock.enrollment_date = date(2020, 3, 1)
        mock.gender = 'M'
        mock.full_name = f'{first_name} {last_name}'
        return mock
    
    @staticmethod
    def create_degree(id=1, name='Test Degree'):
        """Create a mock Degree instance."""
        mock = MagicMock()
        mock.id = id
        mock.name = name
        return mock
    
    @staticmethod
    def create_document_type(id=1, name='DNI'):
        """Create a mock DocumentType instance."""
        mock = MagicMock()
        mock.id = id
        mock.name = name
        return mock
    
    @staticmethod
    def create_department(id=1, name='Test Department'):
        """Create a mock Department instance."""
        mock = MagicMock()
        mock.id = id
        mock.name = name
        return mock
    
    @staticmethod
    def create_area(id=1, name='Test Area'):
        """Create a mock Area instance."""
        mock = MagicMock()
        mock.id = id
        mock.name = name
        return mock
    
    @staticmethod
    def create_specialty(id=1, name='Test Specialty'):
        """Create a mock Specialty instance."""
        mock = MagicMock()
        mock.id = id
        mock.name = name
        return mock
    
    @staticmethod
    def create_subject(id=1, name='Test Subject', code='SUB001'):
        """Create a mock Subject instance."""
        mock = MagicMock()
        mock.id = id
        mock.name = name
        mock.code = code
        return mock
    
    @staticmethod
    def create_faculty(id=1, name='Test Faculty'):
        """Create a mock Faculty instance."""
        mock = MagicMock()
        mock.id = id
        mock.name = name
        return mock
    
    @staticmethod
    def create_position(id=1, name='Test Position'):
        """Create a mock Position instance."""
        mock = MagicMock()
        mock.id = id
        mock.name = name
        return mock
    
    @staticmethod
    def create_authority(id=1, name='Test Authority'):
        """Create a mock Authority instance."""
        mock = MagicMock()
        mock.id = id
        mock.name = name
        return mock


class DataFactory:
    """Factory for creating test data dictionaries."""
    
    @staticmethod
    def university_data(**kwargs):
        """Create university test data."""
        data = {
            'name': 'Universidad Nacional de Córdoba',
            'acronym': 'UNC'
        }
        data.update(kwargs)
        return data
    
    @staticmethod
    def student_data(**kwargs):
        """Create student test data."""
        data = {
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'document_number': '12345678',
            'birth_date': date(2000, 1, 1),
            'gender': 'M',
            'student_number': 12345,
            'enrollment_date': date(2020, 3, 1),
            'document_type_id': 1,
            'specialty_id': 1,
        }
        data.update(kwargs)
        return data
    
    @staticmethod
    def degree_data(**kwargs):
        """Create degree test data."""
        data = {
            'name': 'Ingeniería en Sistemas',
            'description': 'Carrera de grado en sistemas'
        }
        data.update(kwargs)
        return data
    
    @staticmethod
    def document_type_data(**kwargs):
        """Create document type test data."""
        data = {
            'name': 'DNI',
            'description': 'Documento Nacional de Identidad'
        }
        data.update(kwargs)
        return data
    
    @staticmethod
    def department_data(**kwargs):
        """Create department test data."""
        data = {
            'name': 'Departamento de Computación',
            'description': 'Departamento de ciencias de la computación'
        }
        data.update(kwargs)
        return data


class MockHelpers:
    """Helper utilities for working with mocks."""
    
    @staticmethod
    def create_mock_queryset(items):
        """Create a mock QuerySet with the given items."""
        mock_qs = MagicMock()
        mock_qs.__iter__ = lambda self: iter(items)
        mock_qs.all.return_value = items
        mock_qs.count.return_value = len(items)
        return mock_qs
    
    @staticmethod
    def create_mock_request(method='GET', data=None, user=None):
        """Create a mock request object."""
        mock_request = MagicMock()
        mock_request.method = method
        mock_request.data = data or {}
        mock_request.user = user or MagicMock()
        return mock_request
    
    @staticmethod
    def create_mock_response(status_code=200, data=None):
        """Create a mock response object."""
        mock_response = MagicMock()
        mock_response.status_code = status_code
        mock_response.data = data or {}
        return mock_response


def skip_if_no_django(test_func):
    """Decorator to skip test if Django is not available."""
    try:
        import django
        return test_func
    except ImportError:
        return unittest.skip("Django not available")(test_func)


def skip_if_no_rest_framework(test_func):
    """Decorator to skip test if Django REST Framework is not available."""
    try:
        import rest_framework
        return test_func
    except ImportError:
        return unittest.skip("Django REST Framework not available")(test_func)
