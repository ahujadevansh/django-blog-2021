import os
import datetime
from django.core import paginator

from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import BadRequest, PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

from .models import Category, Post
from .forms import CategoryForm, PostForm

# Create your views here.
def post(request, slug): 
    # post = Post.query.filter(slug = slug).first()
    # return HttpResponse(f"<h1> {post.title} </h1> <br> <p> {post.content}</p>")
    post = get_object_or_404(Post, slug=slug)
    post.increment_views()
    related_posts = Post.query.filter(author=post.author)[:3]
    context = {
        'post':post,
        'related_posts': related_posts,
    }
    return render(request, "post.html", context)

def index(request):
    latest_posts = Post.query.all().order_by("-created_at")[:6]
    treanding_posts = Post.query.all().order_by("-views")[:3]
    category_1 = Category.query.all()[:1]
    category_2 = Category.query.all()[1:2]
    post_category_1 = Post.query.filter(category=category_1)[:3]
    post_category_2 = Post.query.filter(category=category_2)[:3]


    context = {
        'latest_posts': latest_posts,
        'treanding_posts': treanding_posts,
        'category_1': category_1,
        'category_2': category_2,
        'post_category_1': post_category_1,
        'post_category_2': post_category_2,
        'tab': 'dashboard',
    }
    return render(request, 'index.html', context)

@login_required
def create(request):
    if request.method == 'POST':

        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            post = form.save()
            messages.success(request, f"{post.title} post create successfully")
            return redirect("post", slug=post.slug)
        messages.error(request, f"Error while Creating post")
    else:
        form = PostForm()
    
    context = {
        'form': form,
        'tab': 'create',
    }
    return render(request, "form.html", context)

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
            messages.success(request, f"{post.title} updated successfully")
            return redirect("post", slug=post.slug)
        messages.error(request, "Error occured while updating post")
    else:
        form = PostForm(instance=post)
    context = {
        'form': form,
    }
    return render(request, "form.html", context)

@login_required
def delete(request):
    if request.method == 'POST':
        post = get_object_or_404(Post, slug=request.POST.get("slug", None))
        if request.user != post.author:
            raise PermissionDenied()
        
        post.deleted_at = datetime.datetime.now()
        post.save()
        messages.success(request, f"{post.title} Post Moved to trash")
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
        messages.success(request, f"{post.title} Restored")
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
        messages.success(request, f"{post.title} Post Deleted")
        return redirect("my_posts")
    else:
        raise BadRequest()
        

@login_required
def my_posts(request):

    posts = Post.query.filter(author=request.user)
    paginator = Paginator(posts, 10)
    is_paginated = paginator.num_pages > 1
    page = request.GET.get("page", 1)
    if int(page) > paginator.num_pages:
        page = 1
    page_obj = paginator.page(page)
    context = {
        'is_paginated': is_paginated,
        'page_obj':page_obj,
        'tab': 'my_post',
    }
    return render(request, "posts.html", context)
    
def post_category(request, slug):

    category = get_object_or_404(Category, slug=slug)
    posts = Post.query.filter(category=category)
    paginator = Paginator(posts, 10)
    is_paginated = paginator.num_pages > 1
    page = request.GET.get("page", 1)
    if int(page) > paginator.num_pages:
        page = 1
    page_obj = paginator.page(page)
    context = {
        'is_paginated': is_paginated,
        'page_obj':page_obj,
    }
    return render(request, "posts.html", context)
    

def search(request):

    search = request.GET.get("search", "")
    posts = Post.query.filter(Q(title__icontains=search) | Q(content__icontains=search))
    if not posts:
        messages.info(request, f"No Posts found for search result - {search}")
    paginator = Paginator(posts, 10)
    is_paginated = paginator.num_pages > 1
    page = request.GET.get("page", 1)
    if int(page) > paginator.num_pages:
        page = 1
    page_obj = paginator.page(page)
    context = {
        'search':search,
        'is_paginated': is_paginated,
        'page_obj':page_obj,
    }
    return render(request, "posts.html", context)
    
    
def category(request):
    form = None
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CategoryForm(request.POST)
            if form.is_valid():
                category = form.save()
                messages.success(request, category.name + " Added Succesfully")
        else:
            return redirect('login')
    if(not form):
        form = CategoryForm()

    categories = Category.query.all()
    paginator = Paginator(categories, 10)
    is_paginated = paginator.num_pages > 1
    page = request.GET.get("page", 1)
    if int(page) > paginator.num_pages:
        page = 1
    page_obj = paginator.page(page)
    context = {
        'page_obj': page_obj,
        'is_paginated': is_paginated,
        'form': form,
        'tab': 'categories',
    }
    return render(request, 'categories.html', context)

@login_required
def category_update(request):

    if not request.user.is_staff:
        raise PermissionDenied()

    if request.method == 'POST':
        category = get_object_or_404(Category, slug=request.POST.get("slug", None))
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, category.name + " Updated Succesfully")
            return redirect("category")
    else:
        raise BadRequest()

@login_required
def category_permanent_delete(request):
    if request.method == 'POST':
        category = get_object_or_404(Category.objects, slug=request.POST.get("slug", None))
        if not request.user.is_staff:
            raise PermissionDenied()
        if Post.objects.filter(category=category).count() > 0:
            messages.error(request, category.name + " cannot be deleted. It conntains some posts")
            return redirect("category")
        category.delete()
        messages.success(request, category.name + " Deleted Succesfully")
        return redirect("category")
    else:
        raise BadRequest()