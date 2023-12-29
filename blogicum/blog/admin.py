from django.contrib import admin

from .models import Category, Comment, Location, Post


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


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published')
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_filter = ('is_published',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'post', 'is_published', 'created_at')
    list_editable = ('is_published',)
    search_fields = ('author', 'text')
    list_filter = ('is_published', 'created_at')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
