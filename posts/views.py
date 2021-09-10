from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Category, Post
from .forms import PostForm

# Create your views here.
def post(request, slug): 
    # post = Post.objects.filter(slug = slug).first()
    # return HttpResponse(f"<h1> {post.title} </h1> <br> <p> {post.content}</p>")
    post = get_object_or_404(Post, slug=slug)
    context = {
        'post':post,
    }
    return render(request, "post.html", context)

def index(request):
    posts = Post.objects.all()
    context = {
        'posts' : posts
    }
    return render(request, 'index.html', context)

@login_required
def create(request):
    if request.method == 'POST':

        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            post = form.save()
            return redirect("post", slug=post.slug)
    else:
        form = PostForm()
    
    context = {
        'form': form,
    }
    return render(request, "create.html", context)

@login_required
def update(request, slug):
    
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            # form.instance.author = request.user
            post = form.save()
            return redirect("post", slug=post.slug)
    else:
        form = PostForm(instance=post)
    context = {
        'form': form,
    }
    return render(request, "create.html", context)

@login_required
def my_posts(request):

    posts = Post.objects.filter(author=request.user)
    context = {
        'posts':posts,
    }
    return render(request, "posts.html", context)
    
    