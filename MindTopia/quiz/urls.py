"""URL routing for the quiz application."""

from django.urls import path

from . import views


# URL patterns for quiz pages.
urlpatterns = [
    path("", views.quiz_home, name="questions"),
    path("<int:course_id>/", views.qpage, name="course_quiz"),
]