from django.urls import path
from . import views

urlpatterns = [
    path('titles', views.TitleListAPIView.as_view(), name='title-list'),
    path('titles/<pk>', views.TitleDetailAPIView.as_view(), name='title-detail'),
    path('titles/<title_pk>/chapters/<pk>', views.ChapterDetailAPIView.as_view(), name='chapter-detail'),
    path(
        'titles/<title_pk>/chapters/<pk>/like',
        views.ChapterLikeAPIView.as_view(),
        name='chapter-like'
    ),
]
