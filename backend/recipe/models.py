from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from ingredients.models import Ingredient
from tags.models import Tag


class Recipe(models.Model):
    """ Модель рецептов. """

    author = models.ForeignKey(
        'user.User',  # Использую строковой метод чтобы избежать цикличного
        verbose_name='Автор',  # импорта.
        related_name='recipes_author',
        related_query_name='author',
        on_delete=models.CASCADE
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeInIngredient',
        related_name='recipes_ingredients',
        related_query_name='ingredients'
    )
    tags = models.ManyToManyField(Tag,
                                  related_name='recipes_tags',
                                  related_query_name='tags'
                                  )
    image = models.ImageField('Картинка', upload_to='recipe/images/')
    name = models.CharField('Название', max_length=200, null=False)
    text = models.TextField('Описание', null=False)
    cooking_time = models.IntegerField('Время приготовления', null=False,
                                       validators=[MaxValueValidator(60),
                                                   MinValueValidator(1)
                                                   ])
    favorited_by_users = models.ManyToManyField(
        'user.User',
        through='Favorited',
        related_name='favorited_recipes'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeInIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='recipe_with_ingredient',
                               on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient,
                                   related_name='ingredients_in_recipe',
                                   on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name='Кол-во', validators=[
                                 MinValueValidator(1)])

    class Meta:
        unique_together = ['recipe', 'ingredient']


class ShoppingCart(models.Model):
    """ Модель покупок. """
    user = models.ForeignKey('user.User', verbose_name='Пользователь',
                             on_delete=models.CASCADE,
                             related_name='shopping_cart')
    recipes = models.ManyToManyField(Recipe, related_name='shopping_carts')

    def __str__(self):
        return f"Список покупок пользователя {self.user.username}"


class Favorited(models.Model):
    user = models.ForeignKey('user.User', verbose_name='Пользователь',
                             on_delete=models.CASCADE,
                             related_name='favorited_by_user')
    recipe = models.ForeignKey(Recipe, verbose_name='Рецепт',
                               on_delete=models.CASCADE,
                               related_name='recipes_by_favorited')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'

    def __str__(self):
        return f'Список избранного {self.user.username}-{self.recipe}'
