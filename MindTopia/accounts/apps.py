"""Application configuration for the accounts app."""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Django application configuration for the accounts module.

    This class defines metadata and startup behaviour for the
    accounts application, including loading signal handlers.
    """

    # Default primary key type for models in this app.
    default_auto_field = "django.db.models.BigAutoField"

    # The name of the Django app.
    name = "accounts"

    def ready(self):
        """
        Execute startup code for the accounts application.

        Importing the signals module ensures that signal handlers
        (such as post_save hooks for creating user profiles) are
        registered when Django starts.
        """
        import accounts.signals  # noqa: F401