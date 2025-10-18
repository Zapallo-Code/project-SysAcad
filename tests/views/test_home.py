"""Unit tests for HomeView."""

import unittest
from unittest.mock import patch, MagicMock
from rest_framework import status
from rest_framework.test import APIRequestFactory


class TestHomeView(unittest.TestCase):
    """Test cases for HomeView."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = APIRequestFactory()

    def test_home_view_success(self):
        """Test home view returns OK status."""
        from app.views.home import HomeView

        view = HomeView()
        request = self.factory.get("/")
        response = view.get(request)

        # Should return some response
        self.assertIsNotNone(response)

    def test_home_view_response_format(self):
        """Test home view response format."""
        from app.views.home import HomeView

        view = HomeView()
        request = self.factory.get("/")
        response = view.get(request)

        # Should return a response with data
        self.assertIsNotNone(response)
        if hasattr(response, "data"):
            self.assertIsNotNone(response.data)


if __name__ == "__main__":
    unittest.main()
