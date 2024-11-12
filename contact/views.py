from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from .models import ContactSubmission
from django.core.mail import send_mail
from django.conf import settings
import os


def contact_view(request):
    """
    View to handle contact form submissions.

    Renders the contact form template with a ContactForm instance
    and handles form submission to save messages to the database
    and send emails to the admin.
    """
    admin_email = os.environ.get("EMAIL_ADMIN_ADDRESS")
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            # Save the message to the database
            ContactSubmission.objects.create(
                name=name, email=email, subject=subject, message=message
            )

            # Send email to admin
            send_mail(
                "New Contact Form Submission",
                f"You have received a new message from {name} ({email}):\n\n"
                f"Subject: {subject}\n\n"
                f"{message}",
                settings.DEFAULT_FROM_EMAIL,
                [admin_email],
                fail_silently=False,
            )

            messages.success(
                request, "Your message has been sent successfully."
            )
            return redirect("contact")
    else:
        if request.user.is_authenticated:
            initial_data = {
                "name": request.user.get_full_name(),
                "email": request.user.email,
            }
            form = ContactForm(initial=initial_data)
        else:
            form = ContactForm()

    return render(request, "contact/contact.html", {"form": form})
