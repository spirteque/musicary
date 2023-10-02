from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from .forms import PostCreateForm, SelectSongForm, FindSongForm, CommentForm
from .spotify import get_spotify_details
from .tag_moods import tag_moods
from .models import Post, Comment
from enum import Enum
import logging
from account.views import user_profile

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
                
                friends_ids_list = [(str(user.id), user.username) for user in followings_users]
                friends_ids = tuple(friends_ids_list)
                                
                create_post_form = PostCreateForm(data={'title': title_from_query,
                                                        'song_choice': song_choice_from_query},
                                                songs_ids=songs_ids,
                                                friends_ids=friends_ids)
                
                create_post_form.fields.get('title').widget.attrs['readonly'] = True
                
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
            
            select_song_form.fields.get('title').widget.attrs['readonly'] = True
            
                
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
                
        form_data = request.POST.copy()
        if not 'friend_tags' in form_data:
            form_data['friend_tags'] = 1
        
        create_post_form = PostCreateForm(data=form_data,
                                          friends_ids=friends_ids,
                                          songs_ids=songs_ids)
                 
        if create_post_form.is_valid():
            new_post = create_post_form.save(commit=False)
                        
            new_post.author = request.user
            new_post.name = song['song_name']
            new_post.album = song['song_album']
            new_post.artists = ' | '.join([artist['artist_name'] for artist in song['song_artists']])
            new_post.genre = ' #'.join(song['song_artists_genres'])
            new_post.image = song['song_image']
            new_post.audio = song['song_preview']
            
            new_post.save()
            create_post_form.save_m2m()
            
            for id in create_post_form.cleaned_data['friend_tags']:
                new_post.friend_tags.add(id)
            
            return render(request, 'account/dashboard.html', {'section': 'dashboard',})

    
@login_required
def post_detail(request, post):
    post = get_object_or_404(Post, slug=post)
    
    comments = post.comments.filter(active=True)
    user = request.user
    
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.username = user
            new_comment.save()
            
    else:
        comment_form = CommentForm()
    
    return render(request, 'posts/post/detail.html', {'post': post,
                                                      'comments': comments,
                                                      'form': comment_form})
            
@ajax_required
@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            
            if post.author == request.user:
                return JsonResponse({'status': 'not_updated'})
            
            if action == 'like':
                post.users_like.add(request.user)
            else:
                post.users_like.remove(request.user)
                
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ok'})


@login_required
def delete_post(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    if user == post.author:
        post.delete()
        messages.success(request, 'Post został usunięty.')
    else:
        messages.error(request, 'Nie możesz tego zrobić.')

    return HttpResponseRedirect(f'/account/users/{user.username}/')


@login_required
def delete_friend_tag(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user in post.friend_tags.all():
        post.friend_tags.remove(request.user)
        messages.success(request, 'Oznaczenie zostało usunięte.')
    else:
        messages.error(request, 'Nie możesz tego zrobić.')

    return HttpResponseRedirect(f'/account/users/{request.user.username}/')

@login_required
def delete_comment(request, post_id, comment_id):
    post = Post.objects.get(id=post_id)
    comment = Comment.objects.get(id=comment_id)
    if request.user == comment.username:
        post.comments.remove(comment)
        messages.success(request, 'Komentarz został usunięty.')
    else:
        messages.error(request, 'Nie możesz tego zrobić.')

    return HttpResponseRedirect(f'/posts/details/{post.slug}/')