from django.shortcuts import redirect, render
from .models import Events
# Create your views here.

def home(request):
    event = Events.objects.all()
    return render(request,'all_events.html',{"event":event})


def eventdetials(request,slug):
    event = Events.objects.filter(name=slug)[0]
    return render(request,'event_detail.html',{'event':event})