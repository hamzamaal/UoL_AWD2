"""URL routes for the quiz app."""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.quiz_home, name='questions'),
    path('<int:course_id>/', views.qpage, name='course_quiz'),
]
