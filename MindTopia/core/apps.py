from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Django 4.2+ compatibility
    name = 'core'
