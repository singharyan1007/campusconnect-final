from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="Home"),
    path("editor/<int:id>", views.editor, name="Editor"),
    path("write", views.write, name="Write"),
    path("blog/<int:id>", views.blog, name="blog"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("delete/<int:id>", views.delete, name="Delete"),
]
