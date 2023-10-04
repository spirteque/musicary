from django.urls import path
from main import views

namespace = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('terms/', views.terms, name='terms'),
    path('search/<str:action>/', views.search, name='search'),
    
]
