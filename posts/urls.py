from os import name
from django.urls import path
from . import views as posts_views

# 127.0.0.1:8000/posts/
urlpatterns = [
    path('', posts_views.index, name="posts"),
    path('my_posts/', posts_views.my_posts, name="my_posts"),
    path('create/', posts_views.create, name="create"),
    path('<str:slug>/update/', posts_views.update, name="update"),
    path('delete/', posts_views.delete, name='delete'),
    path('trash/', posts_views.trash, name='trash'),
    path('restore/<str:slug>', posts_views.restore, name='restore'),
    path('permanent_delete/', posts_views.permanent_delete, name='permanent_delete'),
    path('search/', posts_views.search, name='search'),
    path('category/', posts_views.category, name='category'),
    path('category/<str:slug>', posts_views.post_category, name='post_category'),
    path('category_update/', posts_views.category_update, name="category_update"),
    path('category/delete/', posts_views.category_permanent_delete, name="caterogy_delete"),
    # Put it in the last
    path('<str:slug>/', posts_views.post, name="post"),
]