from django.urls import path
from . import views as posts_views

# 127.0.0.1:8000/posts/
urlpatterns = [
    path('<str:slug>/', posts_views.post, name="post"),
    path('', posts_views.index, name="posts")
]