from django.contrib import admin
from .models import ContactSubmission
from django_summernote.admin import SummernoteModelAdmin

class ContactSubmissionAdmin(SummernoteModelAdmin):
    summernote_fields = ('message',)

admin.site.register(ContactSubmission, ContactSubmissionAdmin)
