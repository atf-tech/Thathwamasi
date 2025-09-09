from django.shortcuts import render
from django.http import JsonResponse
from .models import ContactMessage




def index(request):
    return render(request, 'website/index.html')

def about(request):
    return render(request, 'website/about.html')

def service(request):
    return render(request, 'website/service.html')

def portfolio(request):
    return render(request, 'website/portfolio.html')

def contact(request):
    return render(request, 'website/contact.html')




import logging
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import ContactMessage

logger = logging.getLogger(__name__)

@require_POST
def contact_message(request, page_name):
    try:
        name = (request.POST.get("name") or "").strip()
        phone = (request.POST.get("phone") or "").strip()
        email = (request.POST.get("email") or "").strip()
        message = (request.POST.get("message") or "").strip()

        # basic validation
        if not name or not email:
            return JsonResponse(
                {"status": "error", "message": "Name and email are required."},
                status=400,
            )

        ContactMessage.objects.create(
            name=name,
            phone=phone,
            email=email,
            message=message,
            source_page=page_name,
        )

        return JsonResponse({"status": "success", "message": "Message saved successfully!"})

    except Exception as exc:
        # log full traceback to server console / log
        logger.exception("Failed to save contact message")
        # show full error only in DEBUG
        msg = str(exc) if settings.DEBUG else "Internal server error"
        return JsonResponse({"status": "error", "message": msg}, status=500)

