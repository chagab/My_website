import os
from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    intro = models.TextField()
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        upload_to=os.path.join('media', 'blog'),
        default=None,
        null=True,
        blank=True
    )


class Meta:
    ordering = ['-date_added']


class Intro(models.Model):
    body = models.TextField()
