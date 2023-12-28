"""Module with abstract models."""
from django.db import models


class PublishedTimeModel(models.Model):
    """Abstract model. Adds flag is_published and creation date."""

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True


class TitleModel(models.Model):
    """Abstract model. Adds field title and its russian translate."""

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок'
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.title
