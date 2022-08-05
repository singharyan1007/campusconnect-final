from django.shortcuts import redirect, render
from .models import projects
# Create your views here.

def project(request):
    project = projects.objects.all()
    return render(request,'all_projects.html',{"project":project})

def projectdetials(request,slug):
    project = projects.objects.filter(name=slug)[0]
    return render(request,'projects_details.html',{'project':project})