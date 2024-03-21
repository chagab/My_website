from django.shortcuts import render
from .models import Post, Intro
from .static.blog.writing_with_BEC.script import plot_div_dark  # , plot_div_light
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
        'plot_div_dark': plot_div_dark,
        # 'plot_div_light': plot_div_light
    }
    return render(request, 'blog/base.html', context)


def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})
