from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """Form for creating post."""

    class Meta:
        model = Post
        exclude = ('author', 'created_at', 'is_published')
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={'type': 'datetime-local'}
            )
        }


class CommentForm(forms.ModelForm):
    """Form for creating comment."""

    class Meta:
        model = Comment
        fields = ('text',)
