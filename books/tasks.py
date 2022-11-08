from celery import shared_task
from django.db.models import F

from books.models import BookChapter


@shared_task
def increment_like(chapter_pk: int):
    BookChapter.objects.filter(pk=chapter_pk).update(likes=F("likes") + 1)


@shared_task
def increment_views(chapter_pk: int):
    BookChapter.objects.filter(pk=chapter_pk).update(views=F("views") + 1)
