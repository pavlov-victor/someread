from django.urls import reverse
from django.test.utils import override_settings
from rest_framework.test import APITestCase

from books.models import BookTitle, BookChapter, BookVolume


class TestTitle(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.test_data = {
            'name_ru': 'test_title',
            'name_en': 'test_title',
            'name_alternative': 'test_title',
            'description': 'test_description'
        }
        cls.test_object = BookTitle.objects.create(**cls.test_data)

    def test_title_list_e2e(self):
        url = reverse('title-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data['results']) > 0)

    def test_title_detail_e2e(self):
        url = reverse('title-detail', args=[self.test_object.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        for k, v in self.test_data.items():
            self.assertTrue(response.data[k] == v)


class TestChapter(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        title = BookTitle.objects.create(
            name_ru='test_name',
            name_en='test_name',
            name_alternative='test_name',
            description='test_description'
        )
        volume = BookVolume.objects.create(
            title=title,
            number=1,
            name='test_name',
            price=100
        )
        cls.test_data = {
            'volume_id': volume.id,
            'number': 1,
            'content': 'test_content',
        }
        cls.test_object = BookChapter.objects.create(**cls.test_data)

    @override_settings(CELERY_TASK_EAGER_PROPAGATES=True,
                       CELERY_TASK_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory')
    def test_chapter_detail(self):
        url = reverse(
            'chapter-detail',
            kwargs={
                'title_pk': self.test_object.volume.title.pk,
                'pk': self.test_object.pk
            }
        )
        response = self.client.get(url)
        response_second = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['content'], self.test_data['content'])
        self.assertEqual(response.data['views'], 0)
        self.assertEqual(response_second.data['views'], 1)

    @override_settings(CELERY_TASK_EAGER_PROPAGATES=True,
                       CELERY_TASK_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory')
    def test_chapter_like(self):
        url_like = reverse(
            'chapter-like',
            kwargs={
                'title_pk': self.test_object.volume.title.pk,
                'pk': self.test_object.pk
            }
        )
        url = reverse(
            'chapter-detail',
            kwargs={
                'title_pk': self.test_object.volume.title.pk,
                'pk': self.test_object.pk
            }
        )
        self.client.get(url_like)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['likes'], 1)
