from django.db import models


class Ingredient(models.Model):
    name = models.CharField('Имя ингридиента', max_length=200)
    measurement_unit = models.CharField('Единица измерения', max_length=200)

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингриденты'
