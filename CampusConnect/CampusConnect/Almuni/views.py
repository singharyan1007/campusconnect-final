from django.shortcuts import render,HttpResponse,redirect
from urllib3 import HTTPResponse
from .models import Almuni
from django.contrib import messages
# Create your views here.

def almuni(request):
    almuni = Almuni.objects.all()
    return render(request,'alumni.html',{'almuni':almuni})

def alumniform(request):
    return render(request,'alumniform.html')

def alumniconnect(request):
    if request.method =='POST':
        print (request.POST['seat_number'],)
        alumni = Almuni(
            name = request.POST['full_name'],
            designation = request.POST['job_title'],
            company = request.POST['company'],
            branch = request.POST['department'],
            year = request.POST['graduation_year'],
            main_image = request.FILES.get("profilepic"),
            instagram = request.POST["instagram"],
            linkedin = request.POST["linkedin"],
            mail = request.POST['email'],
            USN = request.POST['seat_number'],
            contact = request.POST['contact_number']
        )
        alumni.save()
        messages.info(request,"Thank you for joining back with the college\n, your profile will be verified and confirmed")
        return redirect('/almuni')
    else:
        return HTTPResponse("404_page not found")