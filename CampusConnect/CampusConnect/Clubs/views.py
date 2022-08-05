from django.shortcuts import redirect, render
from .models import Clubs
# Create your views here.

def home(request):
    club = Clubs.objects.all()
    return render(request,'all_clubs.html',{"club":club})