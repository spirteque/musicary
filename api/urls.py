from django.urls import path
from . import views

namespace = 'api'

urlpatterns = [
    path('artist/search', views.search_artist, name='api_search_artist'),
    path('song/search', views.search_song, name='api_search_song'),
]