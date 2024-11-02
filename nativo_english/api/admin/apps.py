from django.apps import AppConfig


class AdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nativo_english.api.admin'  # Ensure this matches your project structure
    label = 'admin_app'  # Unique label for this app
    verbose_name = "Admin Management"  # Optional