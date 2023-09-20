from django import forms
from django.forms.utils import ErrorList
from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _
from .models import Post

ErrorList.template_name = "main/errors.html"

class PostCreateForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'id': 'title_input'}
        )
    )
    
    album = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'id': 'album_input'}
        )
    )
    
    artist = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'id': 'artist_input'}
        )
    )
    
    genre = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'id': 'genre_input'}
        )
    )
    
    author_tags = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'id': 'author_tags_input'}
        )
    )
    
    friend_tags = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={'class': 'form-control',
                   'id': 'friend_tags_input'}
        )
    )
    
    image = forms.ImageField(
        error_messages={'invalid_image': _('Prześlij poprawny obraz, np. w formacie .png, .jpeg.')})
        
    ClearableFileInput.template_name = "main/clearable_file_input.html"
    
    class Meta:
        model = Post
        fields = ('title', 'album', 'artist', 'genre', 'author_tags', 'friend_tags', 'image')