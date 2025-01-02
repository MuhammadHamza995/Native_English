from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nativo_english.api.shared.notifications'

    def ready(self):
        import nativo_english.api.shared.notifications.signals  # Import the signals module