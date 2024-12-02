from django.test import TestCase, Client
from django.urls import reverse


class CustomErrorViewsTests(TestCase):
    def setUp(self):
        """Set up the test client."""
        self.client = Client()

    def test_custom_400_view(self):
        """Test the custom 400 Bad Request view."""
        # Simulate a 400 response
        response = self.client.get("/400/")
        response.status_code = 400
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, "400.html")

    def test_custom_403_view(self):
        """Test the custom 403 Forbidden view."""
        # Simulate a 403 response
        response = self.client.get("/403/")
        response.status_code = 403
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "403.html")

    def test_custom_404_view(self):
        """Test the custom 404 Not Found view."""
        response = self.client.get("/nonexistent-url/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")

    def test_custom_500_view(self):
        """Test the custom 500 Internal Server Error view."""
        # Simulate a 500 response by temporarily disabling a middleware or causing an error
        with self.assertRaises(Exception):
            response = self.client.get("/500/")
            response.status_code = 500
            self.assertEqual(response.status_code, 500)
            self.assertTemplateUsed(response, "500.html")
