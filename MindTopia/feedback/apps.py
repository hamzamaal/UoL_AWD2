"""Application configuration for the feedback application."""

from django.apps import AppConfig


class FeedbackConfig(AppConfig):
    """Define configuration settings for the feedback app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "feedback"