"""URL routing for the feedback application."""

from django.urls import path

from . import views


urlpatterns = [
    # Feedback page route
    path("", views.feed, name="feedback"),
]