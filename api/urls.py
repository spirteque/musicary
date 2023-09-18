from django.urls import path
from . import views

namespace = 'api'

urlpatterns = [
    path('music/<artist_id>', views.MusicView.as_view(), name='api_music'),
]