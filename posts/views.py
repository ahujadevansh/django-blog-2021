import os
import datetime

from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import BadRequest, PermissionDenied

from .models import Category, Post
from .forms import PostForm

# Create your views here.
def post(request, slug): 
    # post = Post.query.filter(slug = slug).first()
    # return HttpResponse(f"<h1> {post.title} </h1> <br> <p> {post.content}</p>")
    post = get_object_or_404(Post, slug=slug)
    context = {
        'post':post,
    }
    return render(request, "post.html", context)

def index(request):
    posts = Post.query.all()
    context = {
        'posts' : posts
    }
    return render(request, 'index.html', context)

@login_required
def create(request):
    if request.method == 'POST':

        form = PostForm(request.POST, request.FILES)
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
    cover_pic_path = post.cover_pic.path
    # from django.core.exceptions import PermissionDenied
    if request.user != post.author:
        raise PermissionDenied()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
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
    if request.method == 'POST':
        post = get_object_or_404(Post, slug=request.POST.get("slug", None))
        if request.user != post.author:
            raise PermissionDenied()
        
        post.deleted_at = datetime.datetime.now()
        post.save()
        return redirect("my_posts")
    else:
        raise BadRequest()

@login_required
def trash(request):

    posts = Post.objects.filter(author=request.user).exclude(deleted_at=None)
    context = {
        'posts':posts,
    }
    return render(request, "trash.html", context)

@login_required
def restore(request, slug):
    if request.method == 'GET':
        post = get_object_or_404(Post.objects, slug=slug)
        if request.user != post.author:
            raise PermissionDenied()
     
        post.deleted_at = None
        post.save()
        return redirect("my_posts")
    else:
        raise BadRequest()

@login_required
def permanent_delete(request):
    if request.method == 'POST':
        post = get_object_or_404(Post.objects, slug=request.POST.get("slug", None))
        if request.user != post.author:
            raise PermissionDenied()
        post.delete()
        return redirect("my_posts")
    else:
        raise BadRequest()
        



@login_required
def my_posts(request):

    posts = Post.query.filter(author=request.user)
    context = {
        'posts':posts,
    }
    return render(request, "posts.html", context)
    
    