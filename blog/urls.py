from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
]
