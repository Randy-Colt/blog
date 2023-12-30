from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from core.models import PublishedTimeModel, TitleModel
from .constants import TITLE_TEXT_SLICE, COMMENT_TEXT_SLICE

User = get_user_model()


class Category(PublishedTimeModel, TitleModel):
    """Post category model."""

    description = models.TextField('Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, цифры, дефис и подчёркивание.')
    )

    class Meta:
        """Russian translate."""

        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Location(PublishedTimeModel):
    """Post location model."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название места'
    )

    class Meta:
        """Russian translate."""

        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        return self.name[:TITLE_TEXT_SLICE]


class Post(PublishedTimeModel, TitleModel):
    """Post model."""

    text = models.TextField('Текст')
    image = models.ImageField(
        'Изображение',
        upload_to='images/posts/%Y/%m/%d/',
        blank=True,
        null=True
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем — '
                   'можно делать отложенные публикации.')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )

    class Meta:
        default_related_name = 'posts'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={"post_id": self.pk})


class Comment(PublishedTimeModel):
    """Comment model."""

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост',
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField('Текст комментария')

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return (
            f'Комментарий автора "{self.author}"\n'
            f'к посту "{self.post}",\n'
            f'текст: "{self.text[:COMMENT_TEXT_SLICE]}..."'
        )
