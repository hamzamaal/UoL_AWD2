"""URL configuration for the core application."""

from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),

    # Contact page route
    path("contactus/", views.contactus, name="contactus"),
]