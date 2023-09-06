from django.contrib.auth.models import AbstractUser
from django.db import models
from recipe.models import Recipe


class User(AbstractUser):

    email = models.EmailField('Почта', unique=True, null=False, max_length=254)
    username = models.CharField('Имя пользователя', unique=True, null=False,
                                max_length=150)
    first_name = models.CharField('Имя', null=False, max_length=150)
    last_name = models.CharField('Фамилия', null=False, max_length=150)
    favorites = models.ManyToManyField(
        Recipe,
        related_name='favorited_by',
        blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        related_name='subscriptions',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name='subscribers',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
