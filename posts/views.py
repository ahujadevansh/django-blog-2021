from django.shortcuts import render, HttpResponse
from .models import Category, Post
# Create your views here.
def post(request, slug): 
    post = Post.objects.filter(slug = slug).first()
    return HttpResponse(f"<h1> {post.title} </h1> <br> <p> {post.content}</p>")

def index(request):
    post = Post.objects.all()
    print(post)
    return HttpResponse("Done")
