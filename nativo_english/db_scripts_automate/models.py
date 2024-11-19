from django.db import models

# Create your models here.
class ExecutedSQLScript(models.Model):
    file_name = models.CharField(max_length=255)
    executed_at = models.DateTimeField(auto_now_add=True)
    build_number = models.CharField()