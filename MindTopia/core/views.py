"""Views for the core app."""

from django.shortcuts import render


def home(request):
    """Render the public landing page."""
    return render(request, 'home.html')


def about(request):
    """Render the application's about page."""
    return render(request, 'about.html')
