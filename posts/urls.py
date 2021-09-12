from django.urls import path
from . import views as posts_views

# 127.0.0.1:8000/posts/
urlpatterns = [
    path('', posts_views.index, name="posts"),
    path('my_posts/', posts_views.my_posts, name="my_posts"),
    path('create/', posts_views.create, name="create"),
    path('<str:slug>/update/', posts_views.update, name="update"),
    path('delete/', posts_views.delete, name='delete'),

    # Put it in the last
    path('<str:slug>/', posts_views.post, name="post"),
]