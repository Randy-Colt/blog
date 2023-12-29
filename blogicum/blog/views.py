from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView)

from .forms import PostForm, CommentForm
from .mixins import (
    CommentMixin,
    CommentUpDelMixin,
    ListPostMixin,
    UpDelPostMixin)
from .models import Category, Post, User
from .utils import get_all_posts, get_posts, get_detailed_post


class PostListView(ListPostMixin):
    """Page with all allowed posts."""

    template_name = 'blog/index.html'


class CategoryPostsView(ListPostMixin):
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
            post = get_detailed_post(self.kwargs['post_id'])
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


class PostUpdateView(UpDelPostMixin, UpdateView):
    """Page with the post editing form."""

    form_class = PostForm


class PostDeleteView(UpDelPostMixin, DeleteView):
    """Page with the post deletion."""

    def get_success_url(self):
        return reverse('blog:profile', args=(self.request.user,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_object()
        return context


class ProfileView(ListPostMixin):
    """User profile with information and his posts."""

    template_name = 'blog/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User,
            username=self.kwargs['username'])
        return context

    def get_queryset(self):
        if self.request.user.username == self.kwargs['username']:
            return get_all_posts().filter(
                author__username=self.kwargs['username']
            ).annotate(
                comment_count=Count('comments')
            ).order_by('-pub_date')
        else:
            return get_posts().filter(
                author__username=self.kwargs['username']
            )


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


class CommentCreateView(CommentMixin, CreateView):
    """View for comment create."""

    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)


class CommentUpdateView(CommentUpDelMixin, UpdateView):
    """Page with the comment updating form."""

    form_class = CommentForm


class CommentDeleteView(CommentUpDelMixin, DeleteView):
    """Page with the comment deletion."""

    pass
