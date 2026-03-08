"""Views for the instructors application."""

from django.shortcuts import render

from .models import Instructor


def instruc(request):
    """Render the page displaying all instructors."""
    instructors = Instructor.objects.all()

    context = {
        "ins": instructors,
    }

    return render(request, "instructors.html", context)