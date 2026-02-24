from django.urls import path
from . import views

urlpatterns = [
    # Course List Page
    path('courses/', views.courses, name='courses'),

    # Course Detail Page (Handles Viewing)
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),

    # Fix: Feedback Submission URL
    path('course/<int:course_id>/submit_feedback/', views.submit_feedback, name='submit_feedback'),
]
