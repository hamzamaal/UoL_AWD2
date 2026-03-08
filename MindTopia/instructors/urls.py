"""URL routing for the instructors application."""

from django.urls import path

from . import views


urlpatterns = [
    path("", views.instruc, name="instructors"),
]