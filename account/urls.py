from django.urls import path
from django.contrib.auth import views as auth_views

from .forms import UserLoginForm, UserSetNewPasswordForm, UserPasswordResetForm, UserPasswordChangeForm
from . import views

namespace = 'account'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(authentication_form=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    
    path('edit/password_change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=UserPasswordResetForm), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(form_class=UserSetNewPasswordForm), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/<str:action>/', views.dashboard, name='dashboard'),
    
    
    path('edit/', views.edit, name='edit'),
    path('edit/delete_photo/', views.delete_profile_photo, name='delete_profile_photo'),
    
    path('users/followers_list/<username>/', views.followers_list, name='followers_list'),
    path('users/following_list/<username>/', views.following_list, name='following_list'),
    
    path('users/<username>/', views.user_profile, name='user_profile'),
    path('users/<username>/<str:action>/', views.user_profile, name='user_profile'),
    
    
    path('follow/', views.toggle_follow, name='toggle_follow'),
    
    path('search/', views.user_search, name='user_search'),
]
