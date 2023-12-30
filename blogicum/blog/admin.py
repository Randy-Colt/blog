from django.contrib import admin

from .models import Category, Comment, Location, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'pub_date',
        'created_at',
        'author',
        'location',
        'category',
        'is_published',
    )
    list_editable = (
        'is_published',
        'location',
        'category'
    )
    search_fields = ('title', 'author__username')
    list_filter = ('is_published', 'location', 'category', 'created_at')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'slug',
        'is_published'
    )
    list_editable = ('is_published',)
    search_fields = ('title', 'slug')
    list_filter = ('is_published',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published')
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_filter = ('is_published',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'post', 'is_published', 'created_at')
    list_editable = ('is_published',)
    search_fields = ('author', 'text')
    list_filter = ('is_published', 'created_at')
