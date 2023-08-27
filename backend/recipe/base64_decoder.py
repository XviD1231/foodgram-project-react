from rest_framework import serializers
from django.core.files.base import ContentFile
import base64


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, img = data.split(';base64,')
            ext = format.split('/')[-1]
            decoded_image = base64.b64decode(img)
            data = ContentFile(decoded_image, name=f'Изображение.{ext}')
        return super().to_internal_value(data)
