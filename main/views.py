from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.postgres.search import TrigramSimilarity, SearchVector
from .forms import SearchForm
from posts.models import Post


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
        user_results = User.objects.annotate(similarity=TrigramSimilarity('username', query),
                                             ).filter(similarity__gt=0.1).order_by('-similarity')[:18]
        user_tag_results = Post.objects.annotate(similarity=TrigramSimilarity('friend_tags__username', query),
                                                ).filter(similarity__gt=0.1).order_by('-similarity')[:18]
        
        return render(request, 'main/search_users.html', {'query': query,
                                                          'user_results': user_results,
                                                          'user_tag_results': user_tag_results})
    if action == 'posts':
        post_results = Post.objects.annotate(similarity=TrigramSimilarity('title', query),
                                             ).filter(similarity__gt=0.1).order_by('-similarity')[:9]
        mood_tag_results = Post.objects.annotate(search=SearchVector('author_tags'),
                                                 ).filter(search=query)[:9]
        genre_results = Post.objects.annotate(search=SearchVector('genre'),
                                              ).filter(search=query)[:9]
        
        return render(request, 'main/search_posts.html', {'query': query,
                                                          'post_results': post_results,
                                                          'mood_tag_results': mood_tag_results,
                                                          'genre_results': genre_results})