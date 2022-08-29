from django.urls import path
from . import views


urlpatterns = [
    path("", views.almuni, name="Home"),
    path("connect/", views.alumniform, name="connect"),
    path("form/", views.alumniconnect, name="form"),

]