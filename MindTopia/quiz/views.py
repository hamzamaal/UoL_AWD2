"""View logic for the quiz app."""

from django.shortcuts import get_object_or_404, redirect, render

from courses.models import Course

from .models import Quiz


def quiz_home(request):
    """Redirect to the first course quiz or render an empty quiz page."""
    first_course = Course.objects.filter(quiz_questions__isnull=False).distinct().first()

    if first_course:
        return redirect('course_quiz', course_id=first_course.id)

    return render(request, 'quiz.html', {'questions': [], 'course': None})


def qpage(request, course_id):
    """Display the quiz questions for a specific course."""
    course = get_object_or_404(Course, id=course_id)
    questions = Quiz.objects.filter(course=course)
    return render(request, 'quiz.html', {'questions': questions, 'course': course})
