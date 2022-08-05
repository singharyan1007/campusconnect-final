from django.urls import path
from . import views

urlpatterns = [
    path('',views.project,name='home'),
    path('project_details/<str:slug>',views.projectdetials,name='details')

]
