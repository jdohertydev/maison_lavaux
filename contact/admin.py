from django.contrib import admin
from .models import ContactMessage
from django_summernote.admin import SummernoteModelAdmin

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'replied', 'resolved', 'created_at')
    list_filter = ('replied', 'resolved', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')