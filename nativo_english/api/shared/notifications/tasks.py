# notifications/tasks.py
from celery import shared_task
from django.core.mail import send_mail, get_connection
from django.conf import settings
from django.template import Template, Context
from django.utils.timezone import now
from nativo_english.api.shared.notifications.models import EmailTemplate

from nativo_english.api.shared.user.models import OTP
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email_via_sendgrid(subject, recipient_email, html_content, sender_type="default"):
    """
    Sends an email using SendGrid API.

    Args:
        subject (str): Email subject.
        recipient_email (str): Recipient's email address.
        html_content (str): Email content in HTML format.
        sender_type (str): Either 'default' or 'info' to select the sender.
    """
    try:
        # Select the sender email based on the sender_type
        from_email = (
            settings.SENDGRID_NOTIFY_FROM_EMAIL  # noreply
            if sender_type == "default"
            else settings.SENDGRID_INFO_FROM_EMAIL  # info
        )

        # Construct the email
        message = Mail(
            from_email=from_email,
            to_emails=recipient_email,
            subject=subject,
            html_content=html_content,
        )

        # Send the email
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)

        print(f"Email sent successfully: {response.status_code}")
        return response.status_code

    except Exception as e:
        print(f"Error sending email via SendGrid: {e}")
        raise e
    
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

        # Send the email
        send_email_via_sendgrid (
            subject=subject,
            recipient_email=user_email,
            html_content=rendered_body
        )

    except Exception as e:
        print(f"Error sending email: {e}")