from django.conf import settings
from api.spotify_manager import create_spotify_headers
import requests
import logging

logger = logging.getLogger(__name__)

def spotify_request(url, params=None):
    headers = create_spotify_headers()
    
    if params:
        response = requests.get(url=url,
                            headers=headers,
                            params=params)
    else:
        response = requests.get(url=url, headers=headers)  
        
    logger.info(msg=f'GET {response.url}')
    
    return response

def get_spotify_song_response(title):
    spotify_query_params = {
                'type': 'track',
                'market': 'PL',
                'limit': '6',
                'include_external': 'audio',
                'q': title,
    }
    url = f'{settings.SPOTIFY_API_URL}v1/search'
    spotify_song_response = spotify_request(url=url,
                                            params=spotify_query_params)
    
    return spotify_song_response.json()

def get_songs_ids(spotify_song_response):
    songs_ids = []
    for item in spotify_song_response['tracks']['items']:
        id = item['id']
        songs_ids.append((id, id))
    songs_ids = tuple(songs_ids)
    
    return songs_ids

def get_genres(spotify_song_response):
    artists_ids = set()
    for item in spotify_song_response['tracks']['items']:
        [artists_ids.add(artist['id']) for artist in item['artists']]
            
    genres = []
    for id in artists_ids:
        url = f'{settings.SPOTIFY_API_URL}v1/artists/{id}'
        spotify_artist_response_json = spotify_request(url=url).json()
        genres = spotify_artist_response_json['genres']

        genres.append({'artist_id': id, 'genres': genres})

    return genres

def get_spotify_details(title):
    spotify_song_response = get_spotify_song_response(title)
    songs_ids = get_songs_ids(spotify_song_response)
    genres = get_genres(spotify_song_response)
    
    return [songs_ids, spotify_song_response, genres,]
