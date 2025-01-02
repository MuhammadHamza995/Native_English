from django.db import models
from nativo_english.api.shared.user.models import User

# Create your models here.
class Notification(models.Model):
    NOTIFICATION_CHOICES = [
        ('email', 'Email'),
        ('system', 'System')
    ]

    fk_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications", db_column='fk_user_id'),
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_CHOICES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.fk_user_id.username} - {self.notification_type}"
    

class EmailTemplate(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subject = models.CharField(max_length=255)
    body = models.TextField()  # Store HTML content

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='email_tenmplate_created', db_column='created_by')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='email_tenmplate_modified', db_column='modified_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name