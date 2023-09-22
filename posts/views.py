from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import PostCreateForm, SelectSongForm, FindSongForm
from .spotify import get_spotify_details
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class PostCreateStatus(Enum):
    INIT = 1
    SONG_FOUND = 2
    SONG_FOUND_AND_SELECTED = 3

@login_required
def post_create(request):    
    if request.method == "GET":
        title_from_query = request.GET.get('title')
        song_choice_from_query = request.GET.get('song_choice')
        
        if title_from_query and song_choice_from_query:
            current_status = PostCreateStatus.SONG_FOUND_AND_SELECTED

            [songs_ids, spotify_song_response, genres] = get_spotify_details(title_from_query)
            create_post_form = PostCreateForm(data={'title': title_from_query,
                                                    'song_choice': song_choice_from_query},
                                              songs_ids=songs_ids)
                
            return render(request, 'posts/post/create_pick_song.html', {'form': create_post_form,
                                                                        'current_status': current_status,
                                                                        'search_result': spotify_song_response,
                                                                        'genres': genres})
 
        elif title_from_query:
            current_status = PostCreateStatus.SONG_FOUND
            [songs_ids, spotify_song_response, genres] = get_spotify_details(title_from_query)
            select_song_form = SelectSongForm(data={'title': title_from_query},
                                              songs_ids=songs_ids)
                
            return render(request, 'posts/post/create_pick_song.html', {'form': select_song_form,
                                                                        'current_status': current_status,
                                                                        'search_result': spotify_song_response,
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
            