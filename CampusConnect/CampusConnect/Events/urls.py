from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="Home"),
    path('event_details/<str:slug>',views.eventdetials,name='details')
]
