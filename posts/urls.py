from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('create_post/', views.post_create, name='create_post'),
    path('details/<slug:post>/', views.post_detail, name='post_detail'),
]
