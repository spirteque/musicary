from django.db import models
from django.conf import settings
from django.utils.text import slugify
from taggit.managers import TaggableManager

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='posts_created',
                             on_delete=models.CASCADE)
    
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200,
                              blank=True)
    genre = models.CharField(max_length=200,
                             blank=True)
    
    slug = models.SlugField(max_length=200,
                            blank=True)
    url = models.URLField()
    created = models.DateField(auto_now_add=True,
                               db_index=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='posts_liked',
                                        blank=True)
    tags = TaggableManager()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.author}: {self.title}'
    

class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    username = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                      editable=False)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('created',)
        
    def __str__(self):
        return f'Komentarz dodany przez {self.nick} dla posta {self.post}'
    
