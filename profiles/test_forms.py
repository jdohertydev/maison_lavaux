from django.test import TestCase
from django.contrib.auth.models import User
from .forms import UserProfileForm, UserUpdateForm
from .models import UserProfile


class UserProfileFormTests(TestCase):
    def test_valid_user_profile_form_with_all_fields_filled(self):
        form_data = {
            "default_phone_number": "123456789",
            "default_postcode": "12345",
            "default_town_or_city": "Test City",
            "default_street_address1": "123 Test St",
            "default_street_address2": "Apt 4B",
            "default_county": "Test County",
        }
        form = UserProfileForm(data=form_data)
        self.assertTrue(
            form.is_valid(),
            "UserProfileForm should be valid with all fields filled.",
        )

    def test_valid_user_profile_form_with_optional_fields_missing(self):
        form_data = {
            "default_phone_number": "",
            "default_postcode": "",
            "default_town_or_city": "Test City",  # Providing only one field
            "default_street_address1": "123 Test St",
        }
        form = UserProfileForm(data=form_data)
        self.assertTrue(
            form.is_valid(),
            "UserProfileForm should be valid even when optional fields are missing.",
        )

    def test_user_profile_form_placeholders(self):
        form = UserProfileForm()
        expected_placeholders = {
            "default_phone_number": "Phone Number",
            "default_postcode": "Postal Code",
            "default_town_or_city": "Town or City",
            "default_street_address1": "Street Address 1",
            "default_street_address2": "Street Address 2",
            "default_county": "County, State or Locality",
        }
        for field, placeholder in expected_placeholders.items():
            self.assertEqual(
                form.fields[field].widget.attrs["placeholder"],
                placeholder,
                f"Placeholder for {field} is incorrect.",
            )


class UserUpdateFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password",
            first_name="John",
            last_name="Doe",
            email="john@example.com",
        )

    def test_valid_user_update_form(self):
        form_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
        }
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(
            form.is_valid(),
            "UserUpdateForm should be valid with correct data.",
        )

    def test_invalid_user_update_form_invalid_email(self):
        form_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "invalid-email",
        }
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertFalse(
            form.is_valid(),
            "UserUpdateForm should be invalid with an incorrect email address.",
        )
        self.assertIn("email", form.errors)

    def test_user_update_form_placeholders(self):
        form = UserUpdateForm()
        expected_placeholders = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email Address",
        }
        for field, placeholder in expected_placeholders.items():
            self.assertEqual(
                form.fields[field].widget.attrs["placeholder"],
                placeholder,
                f"Placeholder for {field} is incorrect.",
            )
