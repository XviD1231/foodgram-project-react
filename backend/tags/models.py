from django.db import models


class Tag(models.Model):
    name = models.CharField('Имя', max_length=200)
    color = models.CharField('Цвет', max_length=7)
    slug = models.SlugField('Слаг', unique=True, max_length=200)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
