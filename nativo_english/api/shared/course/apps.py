from django.apps import AppConfig


class CourseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nativo_english.api.shared.course'
    label = 'course'  # Unique label for this app
    verbose_name = "Course/Lesson/Content app"  # Optional
