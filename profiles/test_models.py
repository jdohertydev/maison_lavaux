from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileModelTests(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            first_name="John",
            last_name="Doe",
            email="testuser@example.com",
        )

    def test_user_profile_creation(self):
        """
        Test that a UserProfile is automatically created
        when a User is created.
        """
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertIsNotNone(
            user_profile, "UserProfile should be created for a new User."
        )
        self.assertEqual(user_profile.user.username, "testuser")

    def test_user_profile_update(self):
        """
        Test that the UserProfile can be updated successfully.
        """
        user_profile = UserProfile.objects.get(user=self.user)
        user_profile.default_phone_number = "123456789"
        user_profile.default_town_or_city = "Test City"
        user_profile.save()

        updated_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(updated_profile.default_phone_number, "123456789")
        self.assertEqual(updated_profile.default_town_or_city, "Test City")

    def test_user_profile_str_method(self):
        """
        Test the __str__ method of UserProfile returns the username.
        """
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(
            str(user_profile),
            "testuser",
            "The __str__ method should return the username.",
        )

    def test_signal_creates_user_profile(self):
        """
        Test the post_save signal creates a UserProfile.
        """
        new_user = User.objects.create_user(
            username="newuser", password="newpassword"
        )
        user_profile = UserProfile.objects.get(user=new_user)
        self.assertIsNotNone(
            user_profile,
            "UserProfile should be created by the post_save signal.",
        )

    def test_signal_updates_user_profile(self):
        """
        Test the post_save signal updates the UserProfile when the User is updated.
        """
        self.user.first_name = "Jane"
        self.user.save()  # This should trigger the signal
        self.user.refresh_from_db()

        # Verify the profile still exists and is linked to the updated user
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(
            user_profile.user.first_name,
            "Jane",
            "The post_save signal should update the profile.",
        )
