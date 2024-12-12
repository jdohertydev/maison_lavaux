from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from .models import ContactMessage
from .admin import ContactMessageAdmin

class MockRequest:
    """Mock request object for admin tests."""
    pass

class ContactMessageAdminTests(TestCase):
    def setUp(self):
        # Create a mock admin instance and a test contact message
        self.site = AdminSite()
        self.admin = ContactMessageAdmin(ContactMessage, self.site)
        self.message = ContactMessage.objects.create(
            name="John Doe",
            email="johndoe@example.com",
            subject="Test Subject",
            message="This is a test message.",
            replied=False,
            resolved=False,
        )

    def test_list_display(self):
        """Ensure list_display fields are correct."""
        expected_display = (
            "name",
            "email",
            "subject",
            "replied",
            "resolved",
            "created_at",
        )
        self.assertEqual(
            self.admin.list_display,
            expected_display,
            "list_display fields do not match the expected values.",
        )

    def test_list_filter(self):
        """Ensure list_filter fields are correct."""
        expected_filters = ("replied", "resolved", "created_at")
        self.assertEqual(
            self.admin.list_filter,
            expected_filters,
            "list_filter fields do not match the expected values.",
        )

    def test_search_fields(self):
        """Ensure search_fields are set correctly."""
        expected_search_fields = ("name", "email", "subject", "message")
        self.assertEqual(
            self.admin.search_fields,
            expected_search_fields,
            "search_fields do not match the expected values.",
        )

    def test_message_created(self):
        """Test that a contact message is created successfully."""
        self.assertEqual(
            ContactMessage.objects.count(),
            1,
            "Contact message was not created successfully.",
        )
        self.assertEqual(
            self.message.name,
            "John Doe",
            "The name of the contact message does not match the expected value.",
        )
        self.assertEqual(
            self.message.subject,
            "Test Subject",
            "The subject of the contact message does not match the expected value.",
        )

    def test_search_functionality(self):
        """Test the admin search functionality."""
        queryset = self.admin.get_search_results(MockRequest(), ContactMessage.objects.all(), "John")
        self.assertIn(
            self.message,
            queryset[0],
            "Search functionality did not return the expected results.",
        )
