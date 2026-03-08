"""Application configuration for the quiz app."""

from django.apps import AppConfig


class QuizConfig(AppConfig):
    """Configure the quiz application for Django."""

    # Application label used by Django to register the app.
    name = "quiz"