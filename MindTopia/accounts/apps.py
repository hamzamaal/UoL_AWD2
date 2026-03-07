# Import AppConfig which is used to configure application-specific settings in Django
from django.apps import AppConfig

# Define the configuration class for the 'accounts' application
class AccountsConfig(AppConfig):

    # Specify the default primary key field type used for models in this app
    default_auto_field = 'django.db.models.BigAutoField'  # Django 4.2+ Compatibility

    # Define the name of the Django application
    name = 'accounts'

    # The ready() method runs when the Django application is fully loaded
    def ready(self):

        # Import the signals module to ensure signal handlers are registered when the app starts
        import accounts.signals  # Ensures signals are loaded properly