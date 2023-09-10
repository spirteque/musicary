from django.urls import path
from django.contrib.auth import views as auth_views

from .forms import UserLoginForm
from . import views

namespace = 'account'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(authentication_form=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
