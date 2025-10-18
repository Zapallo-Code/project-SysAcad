"""Unit tests for Group repository."""

import unittest
from unittest.mock import patch, MagicMock


class TestGroupRepository(unittest.TestCase):
    """Test cases for GroupRepository."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_group = MagicMock()
        self.mock_group.id = 1
        self.mock_group.name = "Grupo A"
        self.mock_group.code = "GA001"

    @patch("app.repositories.group.Group")
    def test_create_success(self, mock_model):
        """Test creating a group successfully."""
        from app.repositories import GroupRepository

        mock_instance = self.mock_group
        mock_model.return_value = mock_instance

        result = GroupRepository.create(
            {"name": "Grupo A", "code": "GA001", "subject": 1}
        )

        mock_model.assert_called_once_with(name="Grupo A", code="GA001", subject=1)
        mock_instance.full_clean.assert_called_once()
        mock_instance.save.assert_called_once()
        self.assertEqual(result, self.mock_group)

    @patch("app.repositories.group.Group")
    def test_find_by_id_success(self, mock_model):
        """Test finding a group by ID successfully."""
        from app.repositories import GroupRepository

        mock_model.objects.get.return_value = self.mock_group

        result = GroupRepository.find_by_id(1)

        self.assertEqual(result, self.mock_group)

    @patch("app.repositories.group.Group")
    def test_find_by_subject(self, mock_model):
        """Test finding groups by subject."""
        from app.repositories import GroupRepository

        mock_model.objects.filter.return_value = [self.mock_group]

        result = GroupRepository.find_by_subject(1)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Grupo A")

    @patch("app.repositories.group.Group")
    def test_find_by_code(self, mock_model):
        """Test finding group by code."""
        from app.repositories import GroupRepository

        mock_model.objects.filter.return_value.first.return_value = self.mock_group

        result = GroupRepository.find_by_code("GA001")

        self.assertEqual(result.code, "GA001")

    @patch("app.repositories.group.Group")
    def test_find_all(self, mock_model):
        """Test finding all groups."""
        from app.repositories import GroupRepository

        mock_model.objects.all.return_value = [self.mock_group]

        result = GroupRepository.find_all()

        self.assertEqual(len(result), 1)

    @patch("app.repositories.group.Group")
    def test_update_success(self, mock_model):
        """Test updating a group successfully."""
        from app.repositories import GroupRepository

        mock_model.objects.filter.return_value.update.return_value = 1
        mock_model.objects.get.return_value = self.mock_group

        result = GroupRepository.update(1, {"name": "Grupo A Updated"})

        self.assertEqual(result, self.mock_group)

    @patch("app.repositories.group.Group")
    def test_delete_success(self, mock_model):
        """Test deleting a group successfully."""
        from app.repositories import GroupRepository

        mock_model.objects.filter.return_value.delete.return_value = (1, {})

        result = GroupRepository.delete(1)

        self.assertTrue(result)

    @patch("app.repositories.group.Group")
    def test_exists_by_code(self, mock_model):
        """Test checking if group exists by code."""
        from app.repositories import GroupRepository

        mock_model.objects.filter.return_value.exists.return_value = True

        result = GroupRepository.exists_by_code("GA001")

        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
