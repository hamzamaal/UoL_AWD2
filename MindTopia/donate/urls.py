"""URL routing for the donate application."""

from django.urls import path

from . import views


urlpatterns = [
    # Donation page
    path("", views.pay, name="donate"),
]