from django.shortcuts import render
from .models import Post, Intro
# Create your views here.


def frontpage(request):
    intro = Intro.objects.all()[0]
    posts = Post.objects.all()
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context = {
        'intro': intro,
        'posts': posts,
        'ip': ip
    }
    return render(request, 'blog/base.html', context)


def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})
