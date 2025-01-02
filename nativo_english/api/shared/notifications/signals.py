# nativo_english/api/notifications/signals.py
from django.db.models.signals import post_save 
from django.dispatch import receiver

from nativo_english.api.shared.user.models import OTP
from nativo_english.api.shared.notifications.tasks import send_otp_email

@receiver(post_save, sender=OTP)
def otp_generated(sender, instance, created, **kwargs):
    if created:
        # Send OTP email asynchronously using Celery
        instance.refresh_from_db()
        send_otp_email.delay(instance.user.email, instance.otp)
