from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import PostCreateForm, SelectSongForm, FindSongForm
from .spotify import get_spotify_details
from .tag_moods import tag_moods
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
        
        if title_from_query:
            [songs_ids, songs] = get_spotify_details(title_from_query)

            if song_choice_from_query:
                current_status = PostCreateStatus.SONG_FOUND_AND_SELECTED
                
                followings_users = request.user.following.all()
                
                none_friend_tag = [('1', "Nie oznaczam znajomego.")]
                friends_ids_list = [(str(user.id), user.username) for user in followings_users]
                friends_ids = tuple(none_friend_tag + friends_ids_list)
                                
                create_post_form = PostCreateForm(data={'title': title_from_query,
                                                        'song_choice': song_choice_from_query},
                                                songs_ids=songs_ids,
                                                friends_ids=friends_ids)
                
                for s in songs:
                    if s['song_id'] == song_choice_from_query:
                        song = s
                    
                return render(request, 'posts/post/create_post.html', {'form': create_post_form,
                                                                        'current_status': current_status,
                                                                        'song': song,
                                                                        'tags': tag_moods})
 

            current_status = PostCreateStatus.SONG_FOUND
            select_song_form = SelectSongForm(data={'title': title_from_query},
                                              songs_ids=songs_ids)
                
            return render(request, 'posts/post/create_post.html', {'form': select_song_form,
                                                                   'current_status': current_status,
                                                                   'songs': songs,})
                         
        else:
            current_status = PostCreateStatus.INIT
            find_song_form = FindSongForm()

            return render(request, 'posts/post/create_post.html', {'form': find_song_form,
                                                                   'current_status': current_status})
    
    if request.method == 'POST':
        followings_users = request.user.following.all()
        none_friend_tag = [('1', "Nie oznaczam znajomego.")]
        friends_ids_list = [(str(user.id), user.username) for user in followings_users]
        friends_ids = tuple(none_friend_tag + friends_ids_list)
        
        title_from_query = request.POST.get('title')
        song_choice_from_query = request.POST.get('song_choice')
        [songs_ids, songs] = get_spotify_details(title_from_query)
        
        for s in songs:
            if s['song_id'] == song_choice_from_query:
                song = s
        
        create_post_form = PostCreateForm(data=request.POST,
                                          friends_ids=friends_ids,
                                          songs_ids=songs_ids)
        print(request.POST)
        
        if not create_post_form.is_valid():
            print('??????????????!!!!!!!!!!!!')
            
            
        if create_post_form.is_valid():
            new_post = create_post_form.save(commit=False)
            
            new_post.author = request.user
            new_post.name = song['song_name']
            new_post.album = song['song_album']
            new_post.artists = ' | '.join([artist['artist_name'] for artist in song['song_artists']])
            new_post.genre = song['song_artists_genres']
            new_post.image = song['song_image']
            new_post.audio = song['song_preview']
            new_post.save()
            create_post_form.save_m2m()
            print(create_post_form.cleaned_data)
                
            return render(request, 'account/dashboard.html', {'section': 'dashboard',})
            