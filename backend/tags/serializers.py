from rest_framework import serializers
from tags.models import Tag


class ColorField(serializers.CharField):
    def to_representation(self, value):
        return value


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    color = ColorField(max_length=7)
    slug = serializers.SlugField(max_length=250)

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
