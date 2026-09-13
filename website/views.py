import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .content import (
    ABOUT,
    CONTACT,
    FLAGSHIP_INITIATIVES,
    INNOVATION_AREAS,
    JOURNEY_STEPS,
    SITE,
    WHY_US,
)
from .email_utils import send_contact_email
from .forms import ContactForm

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def health(request):
    return JsonResponse({"status": "ok"})


def home(request):
    context = {
        "site": SITE,
        "about": ABOUT,
        "innovation_areas": INNOVATION_AREAS,
        "flagship_initiatives": FLAGSHIP_INITIATIVES,
        "journey_steps": JOURNEY_STEPS,
        "why_us": WHY_US,
        "contact": CONTACT,
        "form": ContactForm(),
    }
    return render(request, "website/home.html", context)


@require_http_methods(["POST"])
def contact_submit(request):
    form = ContactForm(request.POST)
    if not form.is_valid():
        return JsonResponse(
            {"ok": False, "errors": form.errors.get_json_data()},
            status=400,
        )

    name = form.cleaned_data["name"]
    email = form.cleaned_data["email"]
    message = form.cleaned_data["message"]

    try:
        send_contact_email(name=name, email=email, message=message)
    except Exception:
        logger.exception("Failed to send contact email")
        return JsonResponse(
            {
                "ok": False,
                "message": "We could not send your message right now. Please try again later.",
            },
            status=500,
        )

    return JsonResponse(
        {
            "ok": True,
            "message": "Thank you for reaching out. We will get back to you soon.",
        }
    )
