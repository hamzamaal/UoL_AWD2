"""View logic for the quiz application."""

from django.shortcuts import get_object_or_404, redirect, render

from courses.models import Course
from .models import Quiz


def quiz_home(request):
    """Redirect to the first available course quiz or show an empty page."""
    # Retrieve the first course that has associated quiz questions.
    first_course = Course.objects.filter(
        quiz_questions__isnull=False
    ).distinct().first()

    if first_course:
        return redirect("course_quiz", course_id=first_course.id)

    return render(
        request,
        "quiz.html",
        {"questions": [], "course": None},
    )


def qpage(request, course_id):
    """Render the quiz page for a specific course."""
    course = get_object_or_404(Course, id=course_id)

    # Fetch quiz questions associated with the course.
    questions = Quiz.objects.filter(course=course)

    return render(
        request,
        "quiz.html",
        {"questions": questions, "course": course},
    )