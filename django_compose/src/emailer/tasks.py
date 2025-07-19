from django.core.mail import send_mail
from celery import shared_task
from time import sleep

@shared_task
def send_feedback_email(email_address, message):
    """Sends an email when the feedback form has been submitted."""
    sleep(10)  # Simulate expensive operation that freezes Django
    send_mail(
        "Your Feedback",
        f"\t{message}\n\nThank you!",
        "support@example.com",
        [email_address],
        fail_silently=False,
    )
