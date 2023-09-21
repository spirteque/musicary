from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from api.spotify_manager import create_spotify_headers
from .forms import PostCreateForm, FindSongForm
import requests
import json

@login_required
def post_create(request):
    if request.method == 'POST':
        form_search = FindSongForm(data=request.POST)
        form_pick = PostCreateForm(data=request.POST)

        if form_search.is_valid():
            cd = form_search.cleaned_data
            song_title = cd['title']
            
            spotify_query_params = {
                'type': 'track',
                'market': 'PL',
                'limit': '6',
                'include_external': 'audio',
                'q': song_title,
            }
            url = f'{settings.SPOTIFY_API_URL}v1/search'
            spotify_song_response = requests.get(url=url,
                                            headers=create_spotify_headers(),
                                            params=spotify_query_params)
            song_search_result = spotify_song_response.json()
            
            artists_id = []
            for item in song_search_result['tracks']['items']:
                for artist in item['artists']:
                    artists_id.append(artist['id'])
            
            genres_raw = []
            for id in artists_id:
                url = f'{settings.SPOTIFY_API_URL}v1/artists/{id}'
                spotify_artist_response = requests.get(url=url, headers=create_spotify_headers())
                artist_search_result_id = spotify_artist_response.json()['id']
                artist_search_result_genres = spotify_artist_response.json()['genres']
                genres_raw.append({'id': artist_search_result_id,
                               'genres': artist_search_result_genres})
            genres = []
            [genres.append(x) for x in genres_raw if x not in genres]
            
            if form_pick.is_valid():
                new_post = form_pick.save(commit=False)
                new_post.author = request.user
                new_post.save()
                
                return render(request, 'account/dashboard.html', {'section': 'dashboard',})
            
            return render(request, 'posts/post/create_pick_song.html', {'section': 'posts',
                                                                        'form_search': form_search,
                                                                        'form_pick': form_pick,
                                                                        'search_result': song_search_result,
                                                                        'genres': genres})    
    else:
        form_search = FindSongForm()
        
    return render(request, 'posts/post/create_search_song.html', {'section': 'posts',
                                                                  'form_search': form_search})