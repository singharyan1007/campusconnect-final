from django.shortcuts import render, HttpResponse, redirect
import requests
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import Account
from Blog.models import Blogpost
from Projects.models import projects
from .forms import AccountForm
# Create your views here.



def signup(request):
    return render(request, 'account/signUp.html')


def handelsignup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        number = request.POST['number']

        if len(password) < 8:
            messages.error(request, "Password should be greater than 8 digits")
            return redirect('/account/Signup')
        if len(number) != 10:
            messages.error(request, "enter a valid number")
            return redirect('/account/Signup')

        checkemail = Account.objects.filter(email=email)
        if checkemail:
            messages.error(request, "e-mail already registered, please use a different id")
            return redirect('/account/Signup')

        try:
            user = Account.objects.create_user(email, username, password)
        except IntegrityError:
            messages.error(request, "Username already taken  please enter a unique Username")
            return redirect('/account/Signup')
        user.name = username
        user.save()
        user = authenticate(request, username=username, password=password)
        html_content = render_to_string("account/welcome.html",{'user':request.user})
        text_content = strip_tags(html_content)
        mail = EmailMultiAlternatives(
            "testing",
            text_content,
            settings.EMAIL_HOST_USER,
            [email ]
        )
        mail.attach_alternative(html_content,"text/html")
        mail.send()
        if user is not None:
            login(request, user)
            return redirect("/")

    else:
        return HttpResponse("404 - Not found")


def loginpage(request):
    return render(request, 'account/login.html')


def handeLogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/account/login")

    return HttpResponse("404- Not found")


def handelLogout(request):
    total = 0
    request.session.get('cart')
    if 'cart' in request.session:
        for p_id, item in request.session['cart'].items():
            total += int(item['qty']) * float(item['price'])
    logout(request)
    return redirect('/')


def profile(request):
    post = Blogpost.objects.filter(user=request.user)
    profile = Account.objects.get(username=request.user)
    project = projects.objects.filter(user=request.user)
    return render(request, 'account/profile.html',{"profile": profile,"post":post,"project":project})


def profiles(request,slug):
    post = Blogpost.objects.filter(user=request.user)
    profile = Account.objects.get(username=request.user)
    project = projects.objects.filter(user=request.user)
    if request.user==slug:
        return render(request, 'account/profile.html',{"profile": profile,"post":post,"project":project})
    else:
        return render(request, 'account/profiles.html',{"profile": profile,"post":post,"project":project})

def profileform(request):
    return render(request,'account/profileform.html')

def updateprofile(request):
    profile = Account.objects.filter(username=request.user)[0]
    if request.method=="POST":
        foi = request.POST.getlist('skills')
        while len(foi)<=5:
            foi.append('')
        profile.image = request.FILES.get('image')
        profile.profil_image = request.FILES.get('image')
        profile.name = request.POST['name']
        profile.surname = request.POST['surname']
        profile.mjskl = request.POST['mjskl']
        profile.github = request.POST['github']
        profile.linkedin = request.POST['linkedin']
        profile.word1 = request.POST['description-1']
        profile.word2 = request.POST['description-2']
        profile.word3 = request.POST['description-3']
        profile.description = request.POST['w3review']
        profile.skills1=foi[0]
        profile.skills2=foi[1]
        profile.skills3=foi[2]
        profile.skills4=foi[3]
        profile.skills5=foi[4]
        profile.save()
        return redirect('/account/profile')
    else:
        return HttpResponse('ERROR 404: PAGE NOT FOUND')

def editprofile(request):
    profile = Account.objects.get(username=request.user)
    form = AccountForm(instance=request.user, data=request.POST)
    if form.is_valid():
        post_item=form.save(commit=False)
        if request.FILES.get("image"):
            image = request.FILES.get("banner")
            post_item.profile_image=image
            post_item.image=image
        post_item.save()
        return redirect("/account/profile")
    else:
        form = AccountForm(instance=request.user)
    return render(request,'account/editprofile.html',{'profile':profile,"form":form})
    