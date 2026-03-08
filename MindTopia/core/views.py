"""Views for the core application."""

from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render


def home(request):
    """Render the public home page."""
    return render(request, "home.html")


def about(request):
    """Render the application about page."""
    return render(request, "about.html")


def contactus(request):
    """Render and process the contact form page."""
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        # Send the message via Django's email system.
        send_mail(
            subject=f"Contact Form: {subject}",
            message=f"Name: {name}\nEmail: {email}\n\n{message}",
            from_email=email,
            recipient_list=["admin@mindtopia.com"],
            fail_silently=True,
        )

        messages.success(request, "Your message has been sent successfully.")

    return render(request, "core/contactus.html")