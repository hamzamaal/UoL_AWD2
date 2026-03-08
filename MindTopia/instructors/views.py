"""Views for the instructors app."""

from django.shortcuts import render

from .models import Instructor


def instruc(request):
    """Display all instructors available on the platform."""
    instructors = Instructor.objects.all()
    return render(request, 'instructo.html', {'ins': instructors})
