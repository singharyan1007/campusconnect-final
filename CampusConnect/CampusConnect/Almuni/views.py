from django.shortcuts import render,HttpResponse
from urllib3 import HTTPResponse
from .models import Almuni

# Create your views here.

def almuni(request):
    almuni = Almuni.objects.all()
    return render(request,'alumni.html',{'almuni':almuni})