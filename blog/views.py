from django.shortcuts import render
from .models import Post, Intro
from .static.blog.writing_with_BEC.makeFigure import plot_div_dark  # , plot_div_light
# Create your views here.


def frontpage(request):
    intro = Intro.objects.all()[0]
    posts = Post.objects.all()
    context = {
        'intro': intro,
        'posts': posts,
        'plot_div_dark': plot_div_dark,
    }
    return render(request, 'blog/base.html', context)


def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})
