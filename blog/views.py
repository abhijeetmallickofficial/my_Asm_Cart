from django.shortcuts import render, get_object_or_404
from .models import BlogPost

def index(request):
    posts = BlogPost.objects.all().order_by('-date_posted')
    return render(request, 'blog/index.html', {'posts': posts})

def blogpost(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'blog/blogpost.html', {'post': post})
