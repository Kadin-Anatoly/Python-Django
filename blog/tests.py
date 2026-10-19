from django.test import TestCase
from django.urls import reverse

from .models import Category, Post


class CategoryModelTest(TestCase):
    def test_str_returns_name(self):
        category = Category.objects.create(name='Python', slug='python')
        self.assertEqual(str(category), 'Python')


class PostModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Python', slug='python')

    def test_str_returns_title(self):
        post = Post.objects.create(
            title='Первая статья',
            slug='first-post',
            text='Текст статьи',
            category=self.category,
        )
        self.assertEqual(str(post), 'Первая статья')

    def test_get_absolute_url(self):
        post = Post.objects.create(
            title='Первая статья',
            slug='first-post',
            text='Текст статьи',
            category=self.category,
        )
        self.assertEqual(post.get_absolute_url(), '/post/first-post/')


class BlogViewTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Python', slug='python')
        Post.objects.create(
            title='Опубликованная статья',
            slug='published-post',
            text='Текст статьи',
            category=category,
            is_published=True,
        )
        Post.objects.create(
            title='Черновик',
            slug='draft-post',
            text='Текст черновика',
            category=category,
            is_published=False,
        )

    def test_index_shows_only_published_posts(self):
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Опубликованная статья')
        self.assertNotContains(response, 'Черновик')

    def test_post_detail_returns_200(self):
        response = self.client.get(reverse('blog:post_detail', args=['published-post']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Текст статьи')

    def test_post_detail_404_for_draft(self):
        response = self.client.get(reverse('blog:post_detail', args=['draft-post']))
        self.assertEqual(response.status_code, 404)

    def test_category_posts_filters_by_category(self):
        response = self.client.get(reverse('blog:category_posts', args=['python']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Опубликованная статья')

    def test_about_returns_200(self):
        response = self.client.get(reverse('blog:about'))
        self.assertEqual(response.status_code, 200)
