from django.shortcuts import render, HttpResponse
from .models import Category, Post
from .forms import PostForm

# Create your views here.
def post(request, slug): 
    post = Post.objects.filter(slug = slug).first()
    return HttpResponse(f"<h1> {post.title} </h1> <br> <p> {post.content}</p>")

def index(request):
    posts = Post.objects.all()
    context = {
        'posts' : posts
    }
    return render(request, 'index.html', context)

def create(request):

    if request.method == 'POST':

        form = PostForm(request.POST)
        post = form.save()
        return HttpResponse(post.title)
    else:
        form = PostForm()
        context = {
            'form': form,
        }
        return render(request, "create.html", context)

