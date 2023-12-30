from datetime import datetime

from django.db.models import Count, QuerySet
from django.shortcuts import get_object_or_404

from .models import Post


def get_all_posts() -> QuerySet:
    """Get all posts with related fields."""
    return Post.objects.select_related(
        'category', 'location', 'author'
    )


def get_detailed_post(post_id: int) -> Post:
    """Filter of one post."""
    return get_object_or_404(
        get_all_posts(),
        pk=post_id,
        is_published=True,
        category__is_published=True,
        pub_date__lte=datetime.now()
    )


def add_annotate_ordering():
    """Add annotate and date sorting to all posts."""
    return get_all_posts().annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')


def get_posts() -> QuerySet:
    """Filtered posts by date and published."""
    return add_annotate_ordering().filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=datetime.now()
            )
