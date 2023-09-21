from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings
from .spotify_manager import create_spotify_headers
import requests
        
    
@api_view(['GET'])
def search_artist(request):
    id = request.query_params['id']
    url = f'{settings.SPOTIFY_API_URL}v1/artists/{id}'

    spotify_response = requests.get(url=url, headers=create_spotify_headers())

    return Response(spotify_response.json())


@api_view(['GET'])
def search_song(request):
    spotify_query_params = {
        'type': 'track',
        'market': 'PL',
        'limit': '6',
        'include_external': 'audio',
        'q': request.query_params['title'],
    }
    url = f'{settings.SPOTIFY_API_URL}v1/search'

    spotify_response = requests.get(url=url,
                                    headers=create_spotify_headers(),
                                    params=spotify_query_params)
    
    return Response(spotify_response.json())

