import datetime

from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import BadRequest, PermissionDenied

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
    # from django.core.exceptions import PermissionDenied
    if request.user != post.author:
        raise PermissionDenied()

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
def delete(request):
    print("->", request.POST)
    if request.method == 'POST':
        print("->", request.POST)
        post = get_object_or_404(Post, slug=request.POST.get("slug", None))
        if request.user != post.author:
            raise PermissionDenied()
        
        post.deleted_at = datetime.datetime.now()
        post.save()
        return redirect("my_posts")
    else:
        raise BadRequest()
        
#     path('delete/', posts_views.delete, name='delete'),


        



@login_required
def my_posts(request):

    posts = Post.objects.filter(author=request.user)
    context = {
        'posts':posts,
    }
    return render(request, "posts.html", context)
    
    