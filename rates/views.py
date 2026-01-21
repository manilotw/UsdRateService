from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta

from .models import USDRate
from .services import fetch_usd_rate


def get_current_usd(request):
    now = timezone.now()
    last_rate = USDRate.objects.order_by('-created_at').first()

    if last_rate:
        diff = now - last_rate.created_at
        if diff < timedelta(seconds=10):
            rate = last_rate.rate
        else:
            rate = fetch_usd_rate()
            USDRate.objects.create(rate=rate)
    else:
        rate = fetch_usd_rate()
        USDRate.objects.create(rate=rate)

    rates = USDRate.objects.order_by('-created_at')
    if rates.count() > 10:
        for item in rates[10:]:
            item.delete()

    history = rates[:10]

    data = {
        "current_rate": float(rate),
        "timestamp": now.isoformat(),
        "history": [
            {
                "rate": float(item.rate),
                "timestamp": item.created_at.isoformat(),
            }
            for item in history
        ]
    }

    return JsonResponse(data)
