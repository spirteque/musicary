from django.conf import settings
from api.spotify_manager import create_spotify_headers
import requests
import logging

logger = logging.getLogger(__name__)

cache = {}

def spotify_request(url, params=None):
    headers = create_spotify_headers()
    
    if params:
        response = requests.get(url=url,
                            headers=headers,
                            params=params)
    else:
        response = requests.get(url=url, headers=headers)  
        
    logger.info(msg=f'"GET {response.url}')
    
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

def get_genres_with_artist_id(spotify_song_response):
    artists_ids = set()
    for item in spotify_song_response['tracks']['items']:
        [artists_ids.add(artist['id']) for artist in item['artists']]
            
    genres = []
    for id in artists_ids:
        
        if id not in cache.keys():
            url = f'{settings.SPOTIFY_API_URL}v1/artists/{id}'
            cache[id] = spotify_request(url=url).json()
            
        artist_genres = cache[id]['genres']
        
        genres.append({'artist_id': id,
                       'artist_genres': artist_genres})

    return genres

def map_to_internal_songs(spotify_song_response, genres_with_artist_id):
    
    songs = spotify_song_response['tracks']['items']
    
    songs_informations = [{'song_id': song['id'],
                           'song_name': song['name'],
                           'song_album': song['album']['name'],
                           'song_image': song['album']['images'][1]['url'],
                           'song_artists': [{'artist_id': artist['id'],
                                             'artist_name': artist['name'],
                                            } for artist in song['artists']
                                           ],
                           'song_artists_genres': [],
                           'song_preview': song['preview_url']
                          } for song in songs]
            
    for song in songs_informations:
        for g_artist in genres_with_artist_id:
            for s_artist in song['song_artists']:
                if s_artist['artist_id'] == g_artist['artist_id']:
                    for genre in g_artist['artist_genres']:
                        song['song_artists_genres'].append(genre)
                    
    return songs_informations

def get_spotify_details(title):
    spotify_song_response = get_spotify_song_response(title)
    songs_ids = get_songs_ids(spotify_song_response)
    genres_with_artist_id = get_genres_with_artist_id(spotify_song_response)
    songs = map_to_internal_songs(spotify_song_response, genres_with_artist_id)
    
    return [songs_ids, songs]
