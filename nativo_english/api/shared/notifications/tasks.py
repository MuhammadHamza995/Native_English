# notifications/tasks.py
from celery import shared_task
from django.core.mail import send_mail, get_connection
from django.conf import settings
from django.template import Template, Context
from django.utils.timezone import now
from nativo_english.api.shared.notifications.models import EmailTemplate

from nativo_english.api.shared.user.models import OTP

@shared_task
def send_email_notification(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        from_email=settings.NOTIFY_EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False
    )


@shared_task 
def send_otp_email(user_email, otp):
    try:
        # Fetch the template from the database
        template = EmailTemplate.objects.get(name="otp_email")
        subject = template.subject
        body = template.body

        # Render the template with dynamic content
        context = {
            "user_name": user_email,
            "otp": otp,
            "otp_validity_minutes": 5,
            "year": now().year,
        }
        rendered_body = Template(body).render(Context(context))

        # Create a custom connection
        connection = get_connection(
            host='smtp.gmail.com',  # or your desired SMTP server
            port=587,
            username=settings.NOTIFY_EMAIL_HOST_USER,
            password=settings.NOTIFY_EMAIL_HOST_PASSWORD,
            use_tls=True
        )
        
        # Send the email using the custom connection
        send_mail(
            subject = subject,
            message="This email requires an HTML viewer.",
            from_email = settings.NOTIFY_EMAIL_HOST_USER,
            recipient_list=[user_email],
            html_message=rendered_body,
            connection=connection
        )

        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")