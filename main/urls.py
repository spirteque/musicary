from django.urls import path
from main import views

namespace = 'main'

urlpatterns = [
    path('', views.test_view, name='test')
]
