"""View logic for the courses application."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from rest_framework import generics
from rest_framework.permissions import AllowAny

from accounts.permissions import IsTeacherUser

from .forms import CourseFeedbackForm
from .models import Course, CourseFeedback
from .serializers import CourseFeedbackSerializer, CourseSerializer


def courses(request):
    """Render the page listing all available courses."""
    return render(
        request,
        "courses/courses.html",
        {"courses": Course.objects.all()},
    )


@login_required
def course_detail(request, course_id):
    """Display a course page and handle feedback submission."""
    course = get_object_or_404(Course, id=course_id)

    feedbacks = CourseFeedback.objects.filter(
        course=course
    ).order_by("-created_at")

    form = CourseFeedbackForm(request.POST or None)

    is_registered = False
    if hasattr(request.user, "userprofile"):
        is_registered = request.user.userprofile.registered_courses.filter(
            id=course.id
        ).exists()

    if request.method == "POST":
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.course = course
            feedback.user = request.user
            feedback.save()

            messages.success(
                request,
                "Your feedback has been submitted successfully!",
            )
            return redirect("course_detail", course_id=course.id)

        messages.error(request, "Error submitting feedback. Please try again.")

    context = {
        "course": course,
        "feedbacks": feedbacks,
        "form": form,
        "is_registered": is_registered,
    }

    return render(request, "courses/course_detail.html", context)


@login_required
def register_course(request, course_id):
    """Allow a student to register for a course."""
    course = get_object_or_404(Course, id=course_id)

    if not hasattr(request.user, "userprofile"):
        messages.error(request, "User profile not found.")
        return redirect("course_detail", course_id=course.id)

    profile = request.user.userprofile

    if profile.role != "student":
        messages.error(request, "Only students can register for courses.")
        return redirect("course_detail", course_id=course.id)

    if profile.registered_courses.filter(id=course.id).exists():
        messages.info(request, "You are already registered for this course.")
    else:
        profile.registered_courses.add(course)
        messages.success(
            request,
            f"You have successfully registered for {course.title}.",
        )

    return redirect("course_detail", course_id=course.id)


@login_required
def submit_feedback(request, course_id):
    """Handle feedback submission from the feedback endpoint."""
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        form = CourseFeedbackForm(request.POST)

        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.course = course
            feedback.user = request.user
            feedback.save()

            messages.success(
                request,
                "Your feedback has been submitted successfully!",
            )
        else:
            messages.error(
                request,
                "Error submitting feedback. Please try again.",
            )

    return redirect("course_detail", course_id=course.id)


class CourseListApiView(generics.ListAPIView):
    """Return a public API list of available courses."""

    queryset = Course.objects.all().order_by("title")
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]


class CourseDetailApiView(generics.RetrieveAPIView):
    """Return public API details for a single course."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]


class CourseFeedbackListApiView(generics.ListAPIView):
    """Return feedback for a course (teacher access only)."""

    serializer_class = CourseFeedbackSerializer
    permission_classes = [IsTeacherUser]

    def get_queryset(self):
        """Return feedback entries for the requested course."""
        return CourseFeedback.objects.filter(
            course_id=self.kwargs["course_id"]
        ).order_by("-created_at")