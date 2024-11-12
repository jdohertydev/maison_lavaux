from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        exclude = ['replied', 'resolved']  # Exclude admin-only fields
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }
