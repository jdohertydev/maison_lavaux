from django.apps import AppConfig


class HomeConfig(AppConfig):
    """
    Configuration class for the Home app, managing app-specific settings.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
