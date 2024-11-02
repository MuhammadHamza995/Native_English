from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nativo_english.api.shared.auth'
    label = 'ne_auth_app'  # Unique label for this app
    verbose_name = "Authentication/login/registration app"  # Optional
