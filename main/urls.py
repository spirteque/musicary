from django.urls import path
from main import views

namespace = 'main'

urlpatterns = [
    path('', views.home, name='home'),
]
