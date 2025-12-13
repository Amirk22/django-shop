from celery import shared_task
from django.core.mail import send_mail
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_verification_email(self, email, subject, message, from_email='noreply@yourdomain.com'):
    try:
        send_mail(
            subject,
            message,
            from_email,
            [email],
            fail_silently=False,
        )
        logger.info(f"Email sent to {email}")
    except Exception as exc:
        logger.error(f"Error sending email to {email}: {exc}")
        raise self.retry(exc=exc)

