from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.postgres.search import TrigramSimilarity
from .forms import SearchForm
from posts.models import Post
import logging

def find_by_similarity(model, by, query, limit=18, similarity_qt=0.1, order_by='-similarity', logger=None):
    results =  model.objects.annotate(similarity=TrigramSimilarity(by, query),).filter(similarity__gt=similarity_qt).order_by(order_by)[:limit]
    
    if logger:
         logger.info(msg=f'Search result in={model.__name__}; by={by}; with query={query}; results={list(results)}')
         
    return results
    

logger = logging.getLogger(__name__)

def home(request):
    return render(request, "main/welcome_page.html")


def terms(request):
    return render(request, 'main/terms.html')


def search(request, action=None):
    if request.method == 'GET':
        query = request.GET.get('query')
        
    if request.method == 'POST':
        form = SearchForm(request.POST)
        
        if form.is_valid():
            query = form.cleaned_data['query']
            
        
    if action == 'users':
        user_results = find_by_similarity(User, 'username', query, logger=logger)
        user_tag_results = find_by_similarity(Post, 'friend_tags__username', query, logger=logger)
        
        return render(request, 'main/search_users.html', {'query': query,
                                                          'user_results': user_results,
                                                          'user_tag_results': user_tag_results})
    if action == 'posts':
        post_results = find_by_similarity(Post, 'name', query, logger=logger, limit=9)
        artist_results = find_by_similarity(Post, 'artists', query, logger=logger, limit=9)
        mood_tag_results = find_by_similarity(Post, 'author_tags', query, logger=logger, limit=9)
        genre_results = find_by_similarity(Post, 'genre', query, logger=logger, limit=9)
        
        return render(request, 'main/search_posts.html', {'query': query,
                                                          'post_results': post_results,
                                                          'artist_results': artist_results,
                                                          'mood_tag_results': mood_tag_results,
                                                          'genre_results': genre_results})