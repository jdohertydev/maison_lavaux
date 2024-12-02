from django.test import TestCase
from .models import ContactMessage


class ContactMessageModelTests(TestCase):
    def setUp(self):
        """Set up a sample ContactMessage for testing."""
        self.contact_message = ContactMessage.objects.create(
            name="John Doe",
            email="johndoe@example.com",
            subject="Test Subject",
            message="This is a test message.",
            replied=False,
            resolved=False,
        )

    def test_string_representation(self):
        """Test the string representation of the ContactMessage model."""
        self.assertEqual(
            str(self.contact_message),
            "Test Subject by John Doe",
            "The __str__ method should return '<subject> by <name>'.",
        )

    def test_default_replied_and_resolved_fields(self):
        """Test that 'replied' and 'resolved' fields default to False."""
        contact_message = ContactMessage.objects.create(
            name="Jane Doe",
            email="janedoe@example.com",
            subject="Another Test Subject",
            message="Another test message.",
        )
        self.assertFalse(contact_message.replied, "The 'replied' field should default to False.")
        self.assertFalse(contact_message.resolved, "The 'resolved' field should default to False.")

    def test_created_at_field(self):
        """Test that 'created_at' is automatically set on creation."""
        self.assertIsNotNone(self.contact_message.created_at, "The 'created_at' field should be automatically set.")
        self.assertTrue(
            hasattr(self.contact_message, "created_at"),
            "The 'created_at' field should exist and be automatically set.",
        )

    def test_model_field_max_lengths(self):
        """Test the max_length of 'name' and 'subject' fields."""
        name_max_length = self.contact_message._meta.get_field("name").max_length
        subject_max_length = self.contact_message._meta.get_field("subject").max_length
        self.assertEqual(name_max_length, 100, "The 'name' field should have max_length 100.")
        self.assertEqual(subject_max_length, 200, "The 'subject' field should have max_length 200.")
