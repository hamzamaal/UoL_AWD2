"""URL routes for the feedback app."""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.feed, name='feedback'),
]
