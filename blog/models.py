from django.db import models
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)
    slug = models.SlugField('Слаг', max_length=110, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField('Слаг', max_length=220, unique=True)
    text = models.TextField('Текст статьи')
    image = models.ImageField('Изображение', upload_to='posts/%Y/%m/', blank=True)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='posts',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    published_at = models.DateTimeField('Дата публикации', default=timezone.now)
    is_published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
