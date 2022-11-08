from rest_framework import serializers

from books.models import BookTitle, BookTag, BookChapter, BookVolume


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookTag
        fields = [
            'id',
            'name',
        ]


class BookTitleListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = BookTitle
        fields = [
            'id',
            'name_ru',
            'name_en',
            'name_alternative',
            'description',
            'tags',
        ]


class BookChapterNestedTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookChapter
        fields = [
            'id',
            'volume',
            'number',
        ]


class BookVolumeNestedTitleSerializer(serializers.ModelSerializer):
    chapters = BookChapterNestedTitleSerializer(many=True, read_only=True)

    class Meta:
        model = BookVolume
        fields = [
            'id',
            'name',
            'number',
            'price',
            'chapters',
        ]


class BookTitleDetailSerializer(serializers.ModelSerializer):
    volumes = BookVolumeNestedTitleSerializer(many=True, read_only=True)

    class Meta:
        model = BookTitle
        fields = [
            'name_ru',
            'name_en',
            'name_alternative',
            'description',
            'tags',
            'volumes',
        ]


class BookChapterDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookChapter
        fields = [
            'volume',
            'number',
            'content',
            'views',
            'likes',
        ]
