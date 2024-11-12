from django import forms
from .models import ContactSubmission
from django_summernote.widgets import SummernoteWidget

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': SummernoteWidget(),
        }
