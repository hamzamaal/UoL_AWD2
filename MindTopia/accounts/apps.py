from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Django 4.2+ Compatibility
    name = 'accounts'

    def ready(self):
        import accounts.signals  # Ensures signals are loaded properly
