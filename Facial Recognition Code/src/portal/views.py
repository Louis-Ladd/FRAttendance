from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
# Create your views here.

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def index(request):
    context = {}

    context["username"] = get_client_ip(request)

    return render(request, "index.html", context)
