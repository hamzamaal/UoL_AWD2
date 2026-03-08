"""Application configuration for the instructors application."""

from django.apps import AppConfig


class InstructorsConfig(AppConfig):
    """Define configuration settings for the instructors app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "instructors"