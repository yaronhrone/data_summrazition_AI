from django.test import TestCase
from django.urls import reverse

from unittest.mock import patch

class HealthCheckTestCase(TestCase):
    """Test case for the health check endpoint."""
    def test_health_check_healthy(self):
        """Test that the health check endpoint returns a healthy status."""
        url = reverse('health_check')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn('status', response.json())
        self.assertIn('healthy', response.json()['status'])
        self.assertEqual(response.json()['status'] , 'healthy')

    @patch("core.views.connection.cursor")
    def test_health_check_db_faliure(self, mock_cursor):
        """Test that the health check endpoint returns an error status when the database is down."""
        mock_cursor.side_effect = Exception("Database connection error")

        url = reverse('health_check')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()['status'] , 'unhealthy')
        self.assertEqual(response.json()["services"]["database"], "failed")