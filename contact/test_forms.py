from django.test import TestCase
from .forms import ContactForm
from .models import ContactMessage


class ContactFormTests(TestCase):
    def test_valid_contact_form(self):
        """Test that the ContactForm is valid with correct data."""
        form_data = {
            "name": "John Doe",
            "email": "johndoe@example.com",
            "subject": "Test Subject",
            "message": "This is a test message.",
        }
        form = ContactForm(data=form_data)
        self.assertTrue(
            form.is_valid(),
            "The ContactForm should be valid with correct data.",
        )

    def test_invalid_contact_form_missing_fields(self):
        """Test that the ContactForm is invalid when required fields are missing."""
        form_data = {
            "name": "",
            "email": "johndoe@example.com",
            "subject": "",
            "message": "",
        }
        form = ContactForm(data=form_data)
        self.assertFalse(
            form.is_valid(),
            "The ContactForm should be invalid when required fields are missing.",
        )
        self.assertIn(
            "name", form.errors, "The 'name' field should be required."
        )
        self.assertIn(
            "subject", form.errors, "The 'subject' field should be required."
        )
        self.assertIn(
            "message", form.errors, "The 'message' field should be required."
        )

    def test_invalid_email_format(self):
        """Test that the ContactForm is invalid with an incorrect email format."""
        form_data = {
            "name": "John Doe",
            "email": "invalid-email",
            "subject": "Test Subject",
            "message": "This is a test message.",
        }
        form = ContactForm(data=form_data)
        self.assertFalse(
            form.is_valid(),
            "The ContactForm should be invalid with an incorrect email format.",
        )
        self.assertIn(
            "email",
            form.errors,
            "The 'email' field should contain an error for invalid format.",
        )

    def test_excluded_fields(self):
        """Test that 'replied' and 'resolved' fields are excluded from the form."""
        form = ContactForm()
        self.assertNotIn(
            "replied",
            form.fields,
            "The 'replied' field should be excluded from the form.",
        )
        self.assertNotIn(
            "resolved",
            form.fields,
            "The 'resolved' field should be excluded from the form.",
        )

    def test_message_widget(self):
        """Test that the 'message' field uses the correct widget."""
        form = ContactForm()
        self.assertEqual(
            form.fields["message"].widget.attrs.get("rows"),
            5,
            "The 'message' field should use a Textarea widget with 5 rows.",
        )
