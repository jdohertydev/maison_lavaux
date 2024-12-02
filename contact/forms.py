from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """
    Form for users to submit contact messages.
    Excludes admin-only fields like 'replied' and 'resolved'.
    """

    class Meta:
        model = ContactMessage
        exclude = ["replied", "resolved"]  # Exclude admin-only fields
        widgets = {
            "message": forms.Textarea(attrs={"rows": 5}),
        }
