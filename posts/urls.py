from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('create_post/', views.post_create, name='create_post'),
    path('details/<slug:post>/', views.post_detail, name='post_detail'),
    path('like/', views.post_like, name='like'),
    path('delete/<post_id>/', views.delete_post, name='delete_post'),
    path('delete_friend_tag/<post_id>/', views.delete_friend_tag, name='delete_friend_tag'),
    
]
