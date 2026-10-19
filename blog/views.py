from django.shortcuts import get_object_or_404, render

from .models import Category, Post


def index(request):
    posts = Post.objects.filter(is_published=True).select_related('category')
    return render(request, 'blog/index.html', {'posts': posts})


def post_detail(request, slug):
    post = get_object_or_404(
        Post.objects.select_related('category').filter(is_published=True),
        slug=slug,
    )
    return render(request, 'blog/post_detail.html', {'post': post})


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.filter(is_published=True)
    return render(request, 'blog/category.html', {'category': category, 'posts': posts})


def about(request):
    return render(request, 'blog/about.html')
