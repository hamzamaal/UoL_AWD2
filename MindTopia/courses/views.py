from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, CourseFeedback
from .forms import CourseFeedbackForm


def courses(request):
    """Displays all available courses"""
    courses = Course.objects.all()
    return render(request, 'courses/courses.html', {'courses': courses})


@login_required
def course_detail(request, course_id):
    """Displays course details and handles feedback submission"""
    course = get_object_or_404(Course, id=course_id)
    feedbacks = CourseFeedback.objects.filter(course=course).order_by('-created_at')

    is_registered = False
    if hasattr(request.user, 'userprofile'):
        is_registered = request.user.userprofile.registered_courses.filter(id=course.id).exists()

    if request.method == "POST":
        form = CourseFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.course = course
            feedback.user = request.user
            feedback.save()
            messages.success(request, "Your feedback has been submitted successfully!")
            return redirect('course_detail', course_id=course.id)
        else:
            messages.error(request, "Error submitting feedback. Please try again.")
    else:
        form = CourseFeedbackForm()

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'feedbacks': feedbacks,
        'form': form,
        'is_registered': is_registered,
    })


@login_required
def register_course(request, course_id):
    """Allows a student to register for a course"""
    course = get_object_or_404(Course, id=course_id)

    if not hasattr(request.user, 'userprofile'):
        messages.error(request, "User profile not found.")
        return redirect('course_detail', course_id=course.id)

    profile = request.user.userprofile

    if profile.role != 'student':
        messages.error(request, "Only students can register for courses.")
        return redirect('course_detail', course_id=course.id)

    if profile.registered_courses.filter(id=course.id).exists():
        messages.info(request, "You are already registered for this course.")
    else:
        profile.registered_courses.add(course)
        messages.success(request, f"You have successfully registered for {course.title}.")

    return redirect('course_detail', course_id=course.id)


@login_required
def submit_feedback(request, course_id):
    """Handles student feedback submission for a course"""
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        form = CourseFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.course = course
            feedback.user = request.user
            feedback.save()
            messages.success(request, "Your feedback has been submitted successfully!")
        else:
            messages.error(request, "Error submitting feedback. Please try again.")

    return redirect('course_detail', course_id=course.id)