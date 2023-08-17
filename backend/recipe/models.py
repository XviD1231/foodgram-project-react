from django.db import models
from ingredients.models import Ingredient
from tags.models import Tag


class Recipe(models.Model):

    author = models.ForeignKey(
        'user.User',
        verbose_name='Автор',
        related_name='recipes_author',
        related_query_name='author',
        on_delete=models.CASCADE
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes_ingredients',
        related_query_name='ingredients'
    )
    tags = models.ManyToManyField(Tag,
                                  related_name='recipes_tags',
                                  related_query_name='tags'
                                  )
    image = models.ImageField('Картинка', null=False, upload_to='api/images/')
    name = models.CharField('Название', max_length=200, null=False)
    text = models.TextField('Описание', null=False)
    cooking_time = models.IntegerField('Время приготовления', null=False)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
