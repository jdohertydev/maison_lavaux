from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    Admin interface for managing contact messages.
    """

    list_display = (
        "name",
        "email",
        "subject",
        "replied",
        "resolved",
        "created_at",
    )
    list_filter = ("replied", "resolved", "created_at")
    search_fields = ("name", "email", "subject", "message")
