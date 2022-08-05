from django.shortcuts import redirect, render
from .models import Blogpost
from django.contrib.auth.models import User
from django.http import HttpResponse
import datetime
from django.contrib import messages
from .forms import PostForm

def home(request):
    blog = Blogpost.objects.all()
    return render(request, 'blog/home.html', {'blog': blog})


def editor(request,id):
    post = Blogpost.objects.filter(post_id=id)[0]
    if request.method == "POST":
        title = request.POST.get("title")
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            post_item=form.save(commit=False)
            post_item.title=title
            post_item.pub_date=datetime.datetime.now()
            if request.FILES.get("banner"):
                image = request.FILES.get("banner")
                post_item.Banner_image=image
            post_item.save()
            return redirect("/blogs/dashboard")
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/editor.html',{"post":post,"form":form})

def write(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            title = request.POST.get("title")
            image = request.FILES.get("banner")
            form=PostForm(request.POST)
            if form.is_valid():
                post_item=form.save(commit=False)
                post_item.user=request.user
                post_item.title=title
                post_item.pub_date=datetime.datetime.now()
                post_item.Banner_image=image
                post_item.save()
            return redirect("/blogs")
        else:
            form = PostForm()
        return render(request, 'blog/write.html',{'form':form})
    else:
        messages.error(request, "Login to continue")
        return redirect("/account/login")

def blog(request, id):
    post = Blogpost.objects.filter(post_id=id)[0]
    try:
        more = Blogpost.objects.filter(post_id=id+1)[0]
        return render(request, 'blog/blog.html', {'post': post, 'more': more})
    except IndexError:
        return render(request, 'blog/blog.html', {'post': post})


def dashboard(request):
    if request.user.is_authenticated:
        post = Blogpost.objects.filter(user=request.user)
        return render(request, 'blog/dashboard.html',{"post":post})
    else:
        return HttpResponse("404-page not found")


def delete(request,id):
    post = Blogpost.objects.filter(post_id=id)[0]
    post.delete()
    return redirect("/blogs/dashboard")