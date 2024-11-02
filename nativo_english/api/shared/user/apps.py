from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nativo_english.api.shared.user'
    label = 'User'  # Unique label for this app
    verbose_name = "User app"  # Optional
