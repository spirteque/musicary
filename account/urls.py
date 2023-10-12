from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views

from .forms import UserLoginForm, UserSetNewPasswordForm, UserPasswordResetForm
from . import views

namespace = 'account'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(authentication_form=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
        
    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=UserPasswordResetForm,
                                                                 from_email=settings.EMAIL_SENDER), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(form_class=UserSetNewPasswordForm), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/<str:action>/', views.dashboard, name='dashboard'),
    
    path('edit/account/', views.edit, name='edit_account'),
    path('edit/delete_image/', views.delete_profile_image, name='delete_profile_image'),
    path('edit/delete_account/', views.delete_account, name='delete_account'),
    path('edit/delete_account_confirm/<uidb64>/<token>/', views.delete_account_confirm, name='delete_account_confirm'),
    path('edit/password_change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('edit/privacy/', views.edit_privacy, name='edit_privacy'),
    
    path('users/followers_list/<username>/', views.followers_list, name='followers_list'),
    path('users/following_list/<username>/', views.following_list, name='following_list'),
    
    path('users/<username>/', views.user_profile, name='user_profile'),
    path('users/<username>/<str:action>/', views.user_profile, name='user_profile'),
    
    path('follow/', views.toggle_follow, name='toggle_follow'),
]
