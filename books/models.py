from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _


class BookTag(models.Model):
    name = models.CharField(_('Tag name'), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'books_tags'
        verbose_name = _('Book tag')
        verbose_name_plural = _('Book tags')


class BookTitle(models.Model):
    name_ru = models.CharField(_('Name ru'), max_length=255)
    name_en = models.CharField(_('Name en'), max_length=255)
    name_alternative = models.CharField(_('Name alternative'), max_length=255)
    description = models.TextField(_('Description'))
    tags = models.ManyToManyField('BookTag', 'titles', verbose_name=_('Tags'), blank=True)

    def __str__(self):
        return self.name_ru

    class Meta:
        db_table = 'books_titles'
        verbose_name = _('Book title')
        verbose_name_plural = _('Book titles')


class BookVolume(models.Model):
    title = models.ForeignKey(
        'BookTitle',
        models.CASCADE,
        related_name='volumes',
        verbose_name=_('Book title'),
    )
    name = models.CharField(_('Volume name'), max_length=255)
    price = models.PositiveIntegerField(_('Price'))
    number = models.PositiveIntegerField(_('Volume number'))

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'books_volumes'
        verbose_name = _('Book volume')
        verbose_name_plural = _('Book volumes')
        constraints = [
            UniqueConstraint(fields=['title', 'number'], name='unique_volume_for_title')
        ]


class BookChapter(models.Model):
    volume = models.ForeignKey(
        'BookVolume',
        models.CASCADE,
        related_name='chapters',
        verbose_name=_('Book chapter'),
    )
    number = models.FloatField(_('Chapter number'))
    content = models.TextField(_('Chapter content'))

    views = models.PositiveIntegerField(_('Chapter views'), default=0)
    likes = models.PositiveIntegerField(_('Chapter likes'), default=0)

    def __str__(self):
        return _('Chapter of') + f' {self.volume}'

    class Meta:
        db_table = 'books_chapters'
        verbose_name = _('Book chapter')
        verbose_name_plural = _('Book chapters')
        constraints = [
            UniqueConstraint(fields=['volume', 'number'], name='unique_chapter_for_volume'),
        ]
