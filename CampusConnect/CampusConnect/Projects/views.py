from django.shortcuts import redirect, render
from urllib3 import HTTPResponse
from django.contrib import messages
from .models import projects
from account.forms import projectForm
# Create your views here.

def project(request):
    project = projects.objects.all()
    return render(request,'all_projects.html',{"project":project})

def addproject(request):
    if request.method =='POST':
        project = projects(
            user = request.user,
            name = request.POST['project'],
            main_image = request.FILES.get("bannerpic"),
            github = request.POST["githublink"],
            deployed_link = request.POST['weblink'],
        )
        form=projectForm(request.POST)
        if form.is_valid():
            proj_item=form.save(commit=False)
            proj_item.user = request.user
            proj_item.name = request.POST['project']
            proj_item.main_image = request.FILES.get("bannerpic")
            proj_item.github = request.POST["githublink"]
            proj_item.deployed_link = request.POST['weblink']
            proj_item.save()
        messages.success(request,"successfully submitted")
        return redirect('/account/profile')
    else:
        return HTTPResponse("404_page not found")


def projectdetials(request,slug):
    project = projects.objects.filter(name=slug)[0]
    return render(request,'projects_details.html',{'project':project})