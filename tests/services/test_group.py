"""Unit tests for Group service."""

import unittest
from unittest.mock import patch, MagicMock


class TestGroupService(unittest.TestCase):
    """Test cases for GroupService."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_group = MagicMock()
        self.mock_group.id = 1
        self.mock_group.name = "Grupo A"
        self.mock_group.code = "GA001"
        self.group_data = {"name": "Grupo A", "code": "GA001", "subject": 1}

    @patch("app.services.group.GroupRepository")
    def test_create_success(self, mock_repo):
        """Test creating a group successfully."""
        from app.services import GroupService

        mock_repo.exists_by_name.return_value = False
        mock_repo.exists_by_code.return_value = False
        mock_repo.create.return_value = self.mock_group

        result = GroupService.create(self.group_data)

        self.assertEqual(result, self.mock_group)
        mock_repo.create.assert_called_once_with(self.group_data)

    @patch("app.services.group.GroupRepository")
    def test_create_duplicate_code(self, mock_repo):
        """Test creating group with duplicate code."""
        from app.services import GroupService

        mock_repo.exists_by_code.return_value = True

        with self.assertRaises(ValueError):
            GroupService.create(self.group_data)

    @patch("app.services.group.GroupRepository")
    def test_find_by_id(self, mock_repo):
        """Test finding group by ID."""
        from app.services import GroupService

        mock_repo.find_by_id.return_value = self.mock_group

        result = GroupService.find_by_id(1)

        self.assertEqual(result, self.mock_group)

    @patch("app.services.group.GroupRepository")
    def test_find_by_subject(self, mock_repo):
        """Test finding groups by subject."""
        from app.services import GroupService

        mock_repo.find_by_subject.return_value = [self.mock_group]

        result = GroupService.find_by_subject(1)

        self.assertEqual(len(result), 1)

    @patch("app.services.group.GroupRepository")
    def test_find_all(self, mock_repo):
        """Test finding all groups."""
        from app.services import GroupService

        mock_repo.find_all.return_value = [self.mock_group]

        result = GroupService.find_all()

        self.assertEqual(len(result), 1)

    @patch("app.services.group.GroupRepository")
    def test_update_success(self, mock_repo):
        """Test updating a group successfully."""
        from app.services import GroupService

        mock_repo.find_by_id.return_value = self.mock_group
        mock_repo.exists_by_name.return_value = False
        mock_repo.update.return_value = self.mock_group

        result = GroupService.update(1, {"name": "Grupo A Updated"})

        self.assertEqual(result, self.mock_group)

    @patch("app.services.group.GroupRepository")
    def test_delete_success(self, mock_repo):
        """Test deleting a group successfully."""
        from app.services import GroupService

        mock_repo.delete.return_value = True

        result = GroupService.delete(1)

        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
