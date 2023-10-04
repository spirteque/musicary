from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.postgres.search import TrigramSimilarity, SearchVector
from .forms import SearchForm
from posts.models import Post


def home(request):
    return render(request, "main/welcome_page.html")


def terms(request):
    return render(request, 'main/terms.html')


def search(request):
    form = SearchForm(request.POST)
    if form.is_valid():
        query = form.cleaned_data['query']
        user_results = User.objects.annotate(similarity=TrigramSimilarity('username', query),).filter(similarity__gt=0.1).order_by('-similarity')[:18]
        user_tag_results = Post.objects.annotate(search=SearchVector('friend_tags__username'),).filter(search=query)[:6]
        post_results = Post.objects.annotate(similarity=TrigramSimilarity('title', query),).filter(similarity__gt=0.1).order_by('-similarity')[:6]
        mood_tag_results = Post.objects.annotate(search=SearchVector('author_tags'),).filter(search=query)[:6]
        genre_results = Post.objects.annotate(search=SearchVector('genre'),).filter(search=query)[:9]
        
    return render(request, 'main/search.html', {'form': form,
                                                'query': query,
                                                'user_results': user_results,
                                                'user_tag_results': user_tag_results,
                                                'post_results': post_results,
                                                'mood_tag_results': mood_tag_results,
                                                'genre_results': genre_results})