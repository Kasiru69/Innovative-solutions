import logging
from email.utils import formataddr

from django.conf import settings
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)


def send_contact_email(*, name: str, email: str, message: str) -> None:
    subject = f"[Innovative Solutions] Message from {name}"
    body = (
        f"You received a new message from the website contact form.\n\n"
        f"Name: {name}\n"
        f"Email: {email}\n\n"
        f"Message:\n{message}"
    )

    email_message = EmailMessage(
        subject=subject,
        body=body,
        from_email=formataddr((name, email)),
        to=[settings.CONTACT_RECIPIENT_EMAIL],
        reply_to=[email],
    )
    email_message.send(fail_silently=False)
    logger.info("Contact email sent to %s from %s", settings.CONTACT_RECIPIENT_EMAIL, email)
