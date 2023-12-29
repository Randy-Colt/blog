from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView

from .models import Comment, Post
from .utils import get_posts

POSTS_PER_PAGE = 10


class ListPostMixin(ListView):
    """Mixin for post list."""

    model = Post
    paginate_by = POSTS_PER_PAGE

    def get_queryset(self):
        return get_posts()


class UpDelPostMixin(LoginRequiredMixin):
    """Mixin for update or delete post."""

    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect(self.get_object().get_absolute_url())
        return super().dispatch(request, *args, **kwargs)


class CommentMixin(LoginRequiredMixin):
    """Mixin for actions with comment."""

    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class CommentUpDelMixin(CommentMixin):
    """Mixin for update or delete comment."""

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', post_id=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)
