from django.urls import path
from . import views

urlpatterns = [
    # Course List Page
    path('courses/', views.courses, name='courses'),

    # Course Detail Page
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),

    # Course Registration
    path('course/<int:course_id>/register/', views.register_course, name='register_course'),

    # Feedback Submission
    path('course/<int:course_id>/submit_feedback/', views.submit_feedback, name='submit_feedback'),

    # Course API Endpoints
    path('api/courses/', views.CourseListApiView.as_view(), name='api_courses'),
    path('api/courses/<int:pk>/', views.CourseDetailApiView.as_view(), name='api_course_detail'),
    path('api/courses/<int:course_id>/feedback/', views.CourseFeedbackListApiView.as_view(), name='api_course_feedback'),
]