"""Unit tests for DedicationType, PositionCategory, SpecialtyType repositories."""
import unittest
from unittest.mock import patch, MagicMock


class TestDedicationTypeRepository(unittest.TestCase):
    """Test cases for DedicationTypeRepository."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_dedication = MagicMock()
        self.mock_dedication.id = 1
        self.mock_dedication.name = 'Dedicación Exclusiva'

    @patch('app.repositories.dedication_type.DedicationType')
    def test_create_success(self, mock_model):
        """Test creating a dedication type successfully."""
        from app.repositories import DedicationTypeRepository
        
        mock_model.objects.create.return_value = self.mock_dedication
        
        result = DedicationTypeRepository.create({'name': 'Dedicación Exclusiva', 'hours': 40})
        
        self.assertEqual(result, self.mock_dedication)

    @patch('app.repositories.dedication_type.DedicationType')
    def test_find_by_id(self, mock_model):
        """Test finding dedication type by ID."""
        from app.repositories import DedicationTypeRepository
        
        mock_model.objects.get.return_value = self.mock_dedication
        
        result = DedicationTypeRepository.find_by_id(1)
        
        self.assertEqual(result, self.mock_dedication)

    @patch('app.repositories.dedication_type.DedicationType')
    def test_find_all(self, mock_model):
        """Test finding all dedication types."""
        from app.repositories import DedicationTypeRepository
        
        mock_model.objects.all.return_value = [self.mock_dedication]
        
        result = DedicationTypeRepository.find_all()
        
        self.assertEqual(len(result), 1)


class TestPositionCategoryRepository(unittest.TestCase):
    """Test cases for PositionCategoryRepository."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_category = MagicMock()
        self.mock_category.id = 1
        self.mock_category.name = 'Profesor Titular'

    @patch('app.repositories.position_category.PositionCategory')
    def test_create_success(self, mock_model):
        """Test creating a position category successfully."""
        from app.repositories import PositionCategoryRepository
        
        mock_model.objects.create.return_value = self.mock_category
        
        result = PositionCategoryRepository.create({'name': 'Profesor Titular'})
        
        self.assertEqual(result, self.mock_category)

    @patch('app.repositories.position_category.PositionCategory')
    def test_find_by_id(self, mock_model):
        """Test finding position category by ID."""
        from app.repositories import PositionCategoryRepository
        
        mock_model.objects.get.return_value = self.mock_category
        
        result = PositionCategoryRepository.find_by_id(1)
        
        self.assertEqual(result, self.mock_category)

    @patch('app.repositories.position_category.PositionCategory')
    def test_find_all(self, mock_model):
        """Test finding all position categories."""
        from app.repositories import PositionCategoryRepository
        
        mock_model.objects.all.return_value = [self.mock_category]
        
        result = PositionCategoryRepository.find_all()
        
        self.assertEqual(len(result), 1)


class TestSpecialtyTypeRepository(unittest.TestCase):
    """Test cases for SpecialtyTypeRepository."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_specialty_type = MagicMock()
        self.mock_specialty_type.id = 1
        self.mock_specialty_type.name = 'Licenciatura'

    @patch('app.repositories.specialty_type.SpecialtyType')
    def test_create_success(self, mock_model):
        """Test creating a specialty type successfully."""
        from app.repositories import SpecialtyTypeRepository
        
        mock_model.objects.create.return_value = self.mock_specialty_type
        
        result = SpecialtyTypeRepository.create({'name': 'Licenciatura'})
        
        self.assertEqual(result, self.mock_specialty_type)

    @patch('app.repositories.specialty_type.SpecialtyType')
    def test_find_by_id(self, mock_model):
        """Test finding specialty type by ID."""
        from app.repositories import SpecialtyTypeRepository
        
        mock_model.objects.get.return_value = self.mock_specialty_type
        
        result = SpecialtyTypeRepository.find_by_id(1)
        
        self.assertEqual(result, self.mock_specialty_type)

    @patch('app.repositories.specialty_type.SpecialtyType')
    def test_find_all(self, mock_model):
        """Test finding all specialty types."""
        from app.repositories import SpecialtyTypeRepository
        
        mock_model.objects.all.return_value = [self.mock_specialty_type]
        
        result = SpecialtyTypeRepository.find_all()
        
        self.assertEqual(len(result), 1)


if __name__ == '__main__':
    unittest.main()
