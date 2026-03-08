"""URL routing for the quiz API application."""

from django.urls import path

from . import views


# API endpoints for quiz resources.
urlpatterns = [
    path("quiz/", views.QuizApiList.as_view(), name="api_quiz_list"),
    path("quiz/<int:pk>/", views.QuizApiDetail.as_view(), name="api_quiz_detail"),
    path(
        "courses/<int:course_id>/quiz/",
        views.QuizByCourseApiList.as_view(),
        name="api_course_quiz_list",
    ),
    # Legacy route maintained for backward compatibility.
    path("", views.QuizApiList.as_view(), name="quizapi_legacy"),
]