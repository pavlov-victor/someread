from django.conf import settings
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import BookTitle, BookChapter
from books.serializers import BookTitleListSerializer, BookTitleDetailSerializer, BookChapterDetailSerializer
from books.tasks import increment_views, increment_like


class TitleListAPIView(ListAPIView):
    queryset = BookTitle.objects.all().prefetch_related('tags')
    serializer_class = BookTitleListSerializer


class TitleDetailAPIView(RetrieveAPIView):
    queryset = BookTitle.objects.all().prefetch_related('volumes__chapters')
    serializer_class = BookTitleDetailSerializer


class ChapterDetailAPIView(RetrieveAPIView):
    queryset = BookChapter.objects.all()
    serializer_class = BookChapterDetailSerializer

    def get_queryset(self):
        return super(ChapterDetailAPIView, self) \
            .get_queryset() \
            .filter(volume__title=self.kwargs['title_pk'])

    def get_object(self):
        obj: BookChapter = super(ChapterDetailAPIView, self).get_object()
        if settings.DEBUG:
            increment_views(obj.pk)
        else:
            increment_views.delay(obj.pk)
        return obj


class ChapterLikeAPIView(APIView):

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(
            BookChapter.objects.all(),
            pk=self.kwargs['pk'],
            volume__title=self.kwargs['title_pk']
        )
        if settings.DEBUG:
            increment_like(obj.pk)
        else:
            increment_like.delay(obj.pk)
        return Response({'status': True}, 200)
