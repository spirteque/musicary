from django.urls import path
from . import views

app_name = 'actions'

urlpatterns = [
    path('', views.show_notifications, name='notifications'),
]