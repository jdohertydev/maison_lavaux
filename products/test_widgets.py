from django.test import TestCase
from django.forms import Form, FileField
from products.widgets import CustomClearableFileInput


class TestCustomClearableFileInput(TestCase):
    def setUp(self):
        """Set up a form for testing the widget."""

        class TestForm(Form):
            image = FileField(widget=CustomClearableFileInput())

        self.form = TestForm()

    def test_widget_attributes(self):
        """Test that the widget attributes are correctly set."""
        widget = CustomClearableFileInput()
        self.assertEqual(widget.clear_checkbox_label, "Remove")
        self.assertEqual(widget.initial_text, "Current Image")
        self.assertEqual(widget.input_text, "")
        self.assertEqual(
            widget.template_name,
            "products/custom_widget_templates/custom_clearable_file_input.html",
        )

    def test_widget_render_in_form(self):
        """Test that the widget renders correctly within a form."""
        rendered = self.form.as_p()
        self.assertIn(
            'id="id_image"', rendered
        )  # Ensures the ID is correctly set
        self.assertIn(
            'name="image"', rendered
        )  # Ensures the name attribute is correctly set
        self.assertIn(
            'type="file"', rendered
        )  # Ensures it is a file input field
