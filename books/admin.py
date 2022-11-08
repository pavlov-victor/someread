from django.contrib import admin

from books.models import BookTitle, BookChapter, BookTag, BookVolume


class BoolVolumeInline(admin.TabularInline):
    model = BookVolume


class BookChapterInline(admin.TabularInline):
    model = BookChapter
    readonly_fields = ['likes', 'views']


@admin.register(BookChapter)
class BookChapterAdmin(admin.ModelAdmin):
    readonly_fields = ['likes', 'views']


@admin.register(BookTag)
class BookTagAdmin(admin.ModelAdmin):
    pass


@admin.register(BookVolume)
class BookVolumeAdmin(admin.ModelAdmin):
    inlines = [BookChapterInline]


@admin.register(BookTitle)
class BookTitleAdmin(admin.ModelAdmin):
    inlines = [BoolVolumeInline]
