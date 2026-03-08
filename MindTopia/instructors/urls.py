"""URL routes for the instructors app."""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.instruc, name='instructors'),
]
