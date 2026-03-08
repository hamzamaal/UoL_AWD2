"""Views for the core application."""

from django.shortcuts import render


def home(request):
    """Render the public home page."""
    return render(request, "home.html")


def about(request):
    """Render the application about page."""
    return render(request, "about.html")