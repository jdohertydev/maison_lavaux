from django.test import TestCase
from .forms import OrderForm


class OrderFormTests(TestCase):
    def setUp(self):
        self.valid_data = {
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "phone_number": "123456789",
            "street_address1": "123 Test St",
            "street_address2": "Apt 4B",
            "town_or_city": "Test City",
            "postcode": "12345",
            "country": "US",
            "county": "Test County",
        }
        self.invalid_data = self.valid_data.copy()
        self.invalid_data["email"] = "not-an-email"  # Invalid email format

    def test_order_form_valid(self):
        """Test the form is valid with correct data."""
        form = OrderForm(data=self.valid_data)
        self.assertTrue(
            form.is_valid(), "OrderForm should be valid with correct data."
        )

    def test_order_form_invalid(self):
        """Test the form is invalid with incorrect data."""
        form = OrderForm(data=self.invalid_data)
        self.assertFalse(
            form.is_valid(), "OrderForm should be invalid with incorrect data."
        )
        self.assertIn(
            "email",
            form.errors,
            "Invalid email should trigger an error on the email field.",
        )

    def test_order_form_placeholders(self):
        """Test the placeholders are correctly set."""
        form = OrderForm()
        expected_placeholders = {
            "full_name": "Full Name *",
            "email": "Email Address *",
            "phone_number": "Phone Number *",
            "postcode": "Postal Code *",
            "town_or_city": "Town or City *",
            "street_address1": "Street Address 1 *",
            "street_address2": "Street Address 2",
            "county": "County, State or Locality",
        }
        for field, placeholder in expected_placeholders.items():
            if (
                field in form.fields and field != "country"
            ):  # Exclude country field
                self.assertEqual(
                    form.fields[field].widget.attrs["placeholder"],
                    placeholder,
                    f"Placeholder for {field} is incorrect.",
                )

    def test_order_form_css_class(self):
        """Test that all fields have the correct CSS class."""
        form = OrderForm()
        for field in form.fields:
            self.assertEqual(
                form.fields[field].widget.attrs["class"],
                "stripe-style-input",
                f"Field {field} does not have the correct CSS class.",
            )

    def test_order_form_autofocus(self):
        """Test that the autofocus is set on the full_name field."""
        form = OrderForm()
        self.assertTrue(
            form.fields["full_name"].widget.attrs.get("autofocus", False),
            "The full_name field should have autofocus set.",
        )
