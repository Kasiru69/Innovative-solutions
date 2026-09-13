import logging

import resend
from django.conf import settings
from resend.exceptions import ResendError

logger = logging.getLogger(__name__)


def send_contact_email(*, name: str, email: str, message: str) -> None:
    if not settings.RESEND_API_KEY:
        raise RuntimeError("RESEND_API_KEY is not configured")

    resend.api_key = settings.RESEND_API_KEY

    subject = f"[Innovative Solutions] Message from {name}"
    text = (
        f"You received a new message from the website contact form.\n\n"
        f"Name: {name}\n"
        f"Email: {email}\n\n"
        f"Message:\n{message}"
    )

    params: resend.Emails.SendParams = {
        "from": settings.RESEND_FROM_EMAIL,
        "to": [settings.CONTACT_RECIPIENT_EMAIL],
        "subject": subject,
        "text": text,
        "reply_to": email,
    }

    try:
        response = resend.Emails.send(params)
    except ResendError:
        logger.exception("Resend API failed to send contact email")
        raise

    logger.info(
        "Contact email sent via Resend (id=%s) to %s, reply_to=%s",
        getattr(response, "id", response),
        settings.CONTACT_RECIPIENT_EMAIL,
        email,
    )
