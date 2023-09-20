from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PostCreateForm

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            
            return render(request, 'account/dashboard.html', {'section': 'dashboard',})
    else:
        form = PostCreateForm()
        
    return render(request, 'posts/post/create.html', {'section': 'posts',
                                                      'form': form})