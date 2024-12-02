from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch
from .models import UserProfile
from checkout.models import Order


class ProfileViewTests(TestCase):
    def setUp(self):
        # Create a test user and profile
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@example.com",
        )
        self.profile = UserProfile.objects.get(user=self.user)

        # Create a sample order linked to the profile
        self.order = Order.objects.create(
            order_number="123456789",
            user_profile=self.profile,
            full_name="John Doe",
            email="testuser@example.com",
            phone_number="123456789",
            country="US",
            postcode="12345",
            town_or_city="Test City",
            street_address1="123 Test St",
            street_address2="Apt 4B",
            county="Test County",
        )

    def test_profile_view_get(self):
        """Test GET request to the profile view."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/profile.html")
        self.assertIn("user_form", response.context)
        self.assertIn("profile_form", response.context)
        self.assertIn("orders", response.context)
        self.assertEqual(len(response.context["orders"]), 1)

    def test_profile_view_post_valid_data(self):
        """Test POST request with valid data to update profile."""
        self.client.login(username="testuser", password="testpassword")
        form_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "default_phone_number": "987654321",
            "default_town_or_city": "New City",
            "default_street_address1": "456 New St",
        }
        response = self.client.post(reverse("profile"), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Profile updated successfully")

        # Verify the profile was updated
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.default_phone_number, "987654321")
        self.assertEqual(self.profile.default_town_or_city, "New City")
        self.assertEqual(self.profile.default_street_address1, "456 New St")

    def test_profile_view_post_invalid_data(self):
        """Test POST request with invalid data."""
        self.client.login(username="testuser", password="testpassword")
        form_data = {"first_name": "", "email": "not-an-email"}  # Invalid data
        response = self.client.post(reverse("profile"), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please correct the errors in the form.")

    def test_profile_view_requires_login(self):
        """Test that the profile view requires login."""
        response = self.client.get(reverse("profile"))
        self.assertNotEqual(response.status_code, 200)  # Should redirect

    def test_order_history_view(self):
        """Test the order history view."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("order_history", args=["123456789"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "checkout/checkout_success.html")
        self.assertIn("order", response.context)
        self.assertEqual(response.context["order"].order_number, "123456789")
        self.assertContains(
            response,
            "This is a past confirmation for order number 123456789.",
        )
