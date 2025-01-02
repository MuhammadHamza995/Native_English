from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from django.conf import settings
import pyotp
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from twilio.rest import Client
import uuid


# Extending the default user setup of Django
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, blank=True, null=True)

    # Override the email field to make it mandatory
    email = models.EmailField(unique=True, blank=False, null=False)
    
class UserPrefs(models.Model):
    fk_user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name="prefs", db_column='fk_user_id')
    enable_2fa = models.BooleanField(default=False)
    otp_secret_key = models.CharField(max_length=255, null=True, blank=True)  # Store the secret key for OTP
    preferred_lang = models.CharField(max_length=7, choices=settings.LANGUAGES, default='en')

    # def generate_otp(self):
    #     otp_obj = OTP.objects.create(user=self.fk_user_id)
    #     otp_obj.generate_otp()

    #     # Send OTP via email
    #     # self.send_otp_email(otp_obj)

    #     # Send OTP via SMS (Twilio example)
    #     # self.send_otp_sms(otp_obj)

    #     return otp_obj

    # def send_otp_email(self, otp_obj):
    #     subject = 'Your OTP for 2FA Login'
    #     message = f"Your OTP is: {otp_obj.otp}. It will expire in 30 seconds."
    #     send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.fk_user.email])

    # def send_otp_sms(self, otp_obj):
    #     # Assuming Twilio is used for SMS
    #     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    #     message = client.messages.create(
    #         body=f"Your OTP is: {otp_obj.otp}. It will expire in 30 seconds.",
    #         from_=settings.TWILIO_PHONE_NUMBER,
    #         to=self.fk_user.phone_number
    #     )

    def __str__(self):
        return f"UserPrefs for {self.fk_user_id.username}"
    

class OTP(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)  # OTP generated
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)  # Track if OTP is used

    def __str__(self):
        return f"OTP for {self.user.email} - {self.otp} (Expires at: {self.expires_at})"
    
    @transaction.atomic
    def generate_otp(self):
         # Check if otp_secret_key is None, and generate one if necessary
        if not self.user.prefs.otp_secret_key:
            self.user.prefs.otp_secret_key = pyotp.random_base32()  # Generate a new secret key
            self.user.prefs.save()  # Save the secret key to the database

        totp = pyotp.TOTP(self.user.prefs.otp_secret_key)
        otp = totp.now()
        self.otp = otp
        self.expires_at = timezone.now() + timedelta(minutes=5)  # Set expires_at to 5 minutes from now
        self.save()  # Save without force_update=True

        # Reload the instance to refresh the in-memory state with the saved OTP
        self.refresh_from_db()

    def is_valid(self):
        # Check if OTP is expired or already used
        if self.is_used:
            return False
        if timezone.now() > self.expires_at:
            return False
        return True

    def mark_as_used(self):
        self.is_used = True
        self.save()

    # def send_otp_email(self, otp_obj):
    #     subject = 'Your OTP for 2FA Login'
    #     message = f"Your OTP is: {otp_obj.otp}. It will expire in 30 seconds."
    #     send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.fk_user.email])

    # def send_otp_sms(self, otp_obj):
    #     # Assuming Twilio is used for SMS
    #     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    #     message = client.messages.create(
    #         body=f"Your OTP is: {otp_obj.otp}. It will expire in 30 seconds.",
    #         from_=settings.TWILIO_PHONE_NUMBER,
    #         to=self.fk_user.phone_number
    #     )


class TempToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    otp = models.OneToOneField(OTP, on_delete=models.CASCADE, related_name="temp_token")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return timezone.now() <= self.expires_at