"""URL routes for the donate app."""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.pay, name='donate'),
]
