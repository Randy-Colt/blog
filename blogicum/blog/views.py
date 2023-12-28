from datetime import datetime
from typing import Any, Type

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.db.models import QuerySet, Count
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView)

from .models import Category, Post, User, Comment
from .forms import PostForm, CommentForm


def get_posts() -> Type[QuerySet]:
    """Filter of posts by date and published."""
    return Post.objects.select_related(
        'category', 'location', 'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=datetime.now()
    ).annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')


class ListPostMixin:
    """Mixin for post list."""

    model = Post
    paginate_by = 10


class PostListView(ListPostMixin, ListView):
    """Page with all allowed posts."""

    template_name = 'blog/index.html'

    def get_queryset(self):
        return get_posts()


class CategoryPostsView(ListPostMixin, ListView):
    """Page with list of posts sorted by one category."""

    template_name = 'blog/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category,
            is_published=True,
            slug=self.kwargs['category_slug']
        )
        return context

    def get_queryset(self):
        return get_posts().filter(
            category__slug=self.kwargs['category_slug']
        )


class PostDetailView(DetailView):
    """Page with detailed post."""

    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        """Check post page by demands."""
        post = super().get_object(queryset)
        if self.request.user != post.author:
            post = get_object_or_404(
                Post,
                pk=self.kwargs['post_id'],
                is_published=True,
                category__is_published=True,
                pub_date__lte=datetime.now()
            )  # нужно ли это как-то оптимизировать?
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related(
            'author'
        ).order_by('created_at')
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Post creation page."""

    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:profile", args=(self.request.user,))


class UpDelPostMixin:
    """Mixin for update or delete post."""

    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        if post.author != request.user:
            return redirect(post.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)


class PostUpdateView(UpDelPostMixin, LoginRequiredMixin, UpdateView):
    """Page with the post editing form."""

    form_class = PostForm


class PostDeleteView(UpDelPostMixin, LoginRequiredMixin, DeleteView):
    """Page with the post deletion."""

    def get_success_url(self):
        return reverse('blog:profile', args=(self.request.user,))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(pk=self.kwargs['post_id'])
        return context


class ProfileView(ListPostMixin, ListView):
    """User profile with information and his posts."""

    template_name = 'blog/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User,
            username=self.kwargs['username'])
        return context

    def get_queryset(self):
        return Post.objects.select_related(
            'category', 'location', 'author'
        ).filter(
            author__username=self.kwargs['username']
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Page with profile update form."""

    model = User
    template_name = 'blog/user.html'
    fields = (
        'username',
        'first_name',
        'last_name',
        'email',
    )

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile', args=(self.request.user,))


class CommentMixin:
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
    """Mixin for update and delete comment."""

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', post_id=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)


class CommentCreateView(CommentMixin, LoginRequiredMixin, CreateView):
    """View for comment create."""

    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)


class CommentUpdateView(CommentUpDelMixin, LoginRequiredMixin, UpdateView):
    """Page with the comment updating form."""

    form_class = CommentForm


class CommentDeleteView(CommentUpDelMixin, LoginRequiredMixin, DeleteView):
    """Page with the comment deletion."""

    pass
