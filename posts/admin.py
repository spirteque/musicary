from django.contrib import admin
from .models import Post, Comment

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'slug', 'created', 'image')
    list_filter = ('author', 'created', 'author_tags')
    search_fields = ('title',)
    raw_id_fields = ('author',)
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('created',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'created', 'active')
    list_filter = ('active', 'created')
    search_fields = ('username', 'body')
