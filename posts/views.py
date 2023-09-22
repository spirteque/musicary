from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from api.spotify_manager import create_spotify_headers
from .forms import PostCreateForm, SelectSongForm, FindSongForm
from enum import Enum
import requests
import logging

logger = logging.getLogger(__name__)

def spotify_request(url, params=None):
    headers = create_spotify_headers()
    print()
    if params:
        return requests.get(url=url,
                            headers=headers,
                            params=params)
    return requests.get(url=url, headers=headers)

def get_spotify_song_response(title):
    spotify_query_params = {
                'type': 'track',
                'market': 'PL',
                'limit': '6',
                'include_external': 'audio',
                'q': title,
    }
    url = f'{settings.SPOTIFY_API_URL}v1/search'
    spotify_song_response = requests.get(url=url,
                                            headers=create_spotify_headers(),
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
    artists_ids = []
    for item in spotify_song_response['tracks']['items']:
        for artist in item['artists']:
            artists_ids.append(artist['id'])
            
    genres_raw = []
    for id in artists_ids:
        url = f'{settings.SPOTIFY_API_URL}v1/artists/{id}'
        spotify_artist_response = requests.get(url=url, headers=create_spotify_headers())
        artist_search_result_id = spotify_artist_response.json()['id']
        artist_search_result_genres = spotify_artist_response.json()['genres']
        genres_raw.append({'id': artist_search_result_id,
                               'genres': artist_search_result_genres})
    genres = []
    [genres.append(x) for x in genres_raw if x not in genres]
    return genres

def get_spotify(title):
    
    spotify_song_response = get_spotify_song_response(title)
    songs_ids = get_songs_ids(spotify_song_response)
    genres = get_genres(spotify_song_response)
    
    return [songs_ids, spotify_song_response, genres,]

@login_required
def post_create(request):

    class PostCreateStatus(Enum):
        INIT = 1
        SONG_FOUND = 2
        SONG_FOUND_AND_SELECTED = 3
    
    if request.method == "GET":
        title_from_query = request.GET.get('title')
        song_choice_from_query = request.GET.get('song_choice')
        
        if title_from_query and song_choice_from_query:
            current_status = PostCreateStatus.SONG_FOUND_AND_SELECTED

            
            [songs_ids, song_search_result, genres] = get_spotify(title_from_query)
            create_post_form = PostCreateForm(data={'title': title_from_query,
                                                    'song_choice': song_choice_from_query},
                                              songs_ids=songs_ids)
                
            return render(request, 'posts/post/create_pick_song.html', {'form': create_post_form,
                                                                            'current_status': current_status,
                                                                            'search_result': song_search_result,
                                                                            'genres': genres})

        
        elif title_from_query:
            current_status = PostCreateStatus.SONG_FOUND
            [songs_ids, song_search_result, genres] = get_spotify(title_from_query)
            select_song_form = SelectSongForm(data={'title': title_from_query},
                                              songs_ids=songs_ids)
                
            return render(request, 'posts/post/create_pick_song.html', {'form': select_song_form,
                                                                            'current_status': current_status,
                                                                            'search_result': song_search_result,
                                                                            'genres': genres})
                
            
        else:
            current_status = PostCreateStatus.INIT
            find_song_form = FindSongForm()

            return render(request, 'posts/post/create_pick_song.html', {'form': find_song_form,
                                                                        'current_status': current_status})
    
    if request.method == 'POST':
        create_post_form = PostCreateForm(data=request.POST)

        if create_post_form.is_valid():
            # new_post = create_post_form.save(commit=False)
            # new_post.author = request.user
            # new_post.save()
            print(create_post_form.cleaned_data)
                
            return render(request, 'account/dashboard.html', {'section': 'dashboard',})
            