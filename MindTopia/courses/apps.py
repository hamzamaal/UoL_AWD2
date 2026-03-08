"""Application configuration for the courses app."""

from django.apps import AppConfig


class CoursesConfig(AppConfig):
    """Configure the courses application."""

    # Default primary key field type for models
    default_auto_field = "django.db.models.BigAutoField"

    # Name of the Django application
    name = "courses"