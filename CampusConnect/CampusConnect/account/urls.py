from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path("Signup/", views.signup, name="signup"),
    path("handelsignup", views.handelsignup, name="handelsignup"),
    path("login/", views.loginpage, name="Login"),
    path('handellogin', views.handeLogin, name="handleLogin"),
    path('logout/', views.handelLogout, name="handleLogout"),
    path('profile/', views.profile, name="profile"),
    path('profiles/<str:slug>',views.profiles,name='profiles'),
    path('profileform', views.profileform, name="profile"),
    path('updateprofile/',views.updateprofile,name="update profile"),
    path('editprofile/',views.editprofile,name="edit profile"),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='account/passwordchangedone.html'),
         name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='account/passwordchange.html'),
         name='password_change'),

    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='account/passwordresetdone.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='account/passwordresetcomplete.html'),
         name='password_reset_complete'),
]
