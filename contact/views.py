from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage
from .forms import ContactForm
import os


def contact_view(request):
    """
    Handles creation of contact submissions.
    Saves the submission to the database and sends an email to the admin.
    """
    # Retrieve admin email from environment variables
    admin_email = os.environ.get("EMAIL_ADMIN_ADDRESS")

    # Meta description for the contact page
    meta_description = (
        "Get in touch with Maison Lavaux. Reach out for inquiries, support, or feedback. "
        "We aim to respond within two working days."
    )

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the form instance and retrieve cleaned data
            contact_message = form.save(commit=False)
            contact_message.save()
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            # Send an email notification to the admin
            send_mail(
                "New Contact Form Submission",
                f"You have received a new message from {name} ({email}):\n\n"
                f"Subject: {subject}\n\n"
                f"{message}",
                settings.DEFAULT_FROM_EMAIL,
                [admin_email],
                fail_silently=False,
            )

            # Provide user feedback and redirect
            messages.success(
                request,
                "Your message has been sent successfully. We will contact you within 2 working days."
            )
            return redirect(reverse("home"))
    else:
        # Pre-fill the form for authenticated users
        if request.user.is_authenticated:
            initial_data = {
                "name": f"{request.user.first_name} {request.user.last_name}",
                "email": request.user.email,
            }
            form = ContactForm(initial=initial_data)
        else:
            form = ContactForm()

    # Render the contact page
    template = "contact/contact.html"
    context = {
        "form": form,
        "meta_description": meta_description,  # Pass meta description to the template
    }
    return render(request, template, context)
