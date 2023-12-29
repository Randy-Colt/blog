from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    """Form for creating post."""

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={'type': 'datetime-local'}
            )
        }


class CommentForm(forms.ModelForm):
    """Form for creating comment."""

    class Meta:
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3})
        }
        model = Comment
        fields = ('text',)
