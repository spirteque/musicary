from django import forms
from django.forms.utils import ErrorList
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectFormField
from .models import Post

ErrorList.template_name = "main/errors.html"

class FindSongForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'id': 'title_input',
                   'placeholder': 'Wyszukaj tytuł piosenki'}
        )
    )
       
    class Meta:
        model = Post
        fields = ('title',)
        

class SelectSongForm(FindSongForm):    
    song_choice = forms.ChoiceField(choices=[],
                                    widget=forms.Select(attrs={'class': 'd-none'}))
    
    def __init__(self, songs_ids, *args, **kwargs):
        super(SelectSongForm, self).__init__(*args, **kwargs)
        
        self.fields['song_choice'].choices = songs_ids
    
    class Meta:
        model = Post
        fields = ('title', 'song_choice')
        

class PostCreateForm(SelectSongForm):    
    friend_tags = MultiSelectFormField(choices=[],
                                        widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
        
    def __init__(self, friends_ids, *args, **kwargs):
        super(PostCreateForm, self).__init__(*args, **kwargs)
        
        self.fields['friend_tags'].choices = friends_ids

    
    class Meta:
        model = Post
        fields = ('title', 'author_tags')