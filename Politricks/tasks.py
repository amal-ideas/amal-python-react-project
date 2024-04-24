from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Post


@shared_task
def count_posts():
    return Post.objects.count()
