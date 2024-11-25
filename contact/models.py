from django.db import models


class ContactMessage(models.Model):
    """
    Model to store contact messages submitted by users.
    Includes fields for message details, reply, and resolution status.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    replied = models.BooleanField(default=False)
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} by {self.name}"
