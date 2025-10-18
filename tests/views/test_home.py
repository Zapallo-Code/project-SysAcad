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

    @patch('app.views.home.HomeView')
    def test_home_view_success(self, mock_view):
        """Test home view returns OK status."""
        from app.views.home import HomeView
        
        view = HomeView()
        request = self.factory.get('/')
        response = view.get(request)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)
        self.assertEqual(response.data['status'], 'OK')

    @patch('app.views.home.logger')
    @patch('app.views.home.HomeView.get')
    def test_home_view_error_handling(self, mock_get, mock_logger):
        """Test home view error handling."""
        from app.views.home import HomeView
        from rest_framework.response import Response
        
        mock_get.side_effect = Exception('Test error')
        
        view = HomeView()
        request = self.factory.get('/')
        
        try:
            response = view.get(request)
        except Exception:
            # Exception expected
            pass

    @patch('app.views.home.HomeView')
    def test_home_view_response_format(self, mock_view):
        """Test home view response format."""
        from app.views.home import HomeView
        
        view = HomeView()
        request = self.factory.get('/')
        response = view.get(request)
        
        self.assertIsInstance(response.data, dict)


if __name__ == '__main__':
    unittest.main()
