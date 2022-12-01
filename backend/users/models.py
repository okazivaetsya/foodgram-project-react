from django.db import models
from django.contrib.auth.models import AbstractUser


class FoodgramUser(AbstractUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=254,
        blank=False,
        unique=True,
    )
    username = models.CharField(
        verbose_name='Уникальное имя',
        max_length=150,
        blank=False,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=False,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=False,
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150,
        blank=False,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        null=True,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        null=True,
        related_name='following',
        verbose_name='Автор рецепта'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_following'
            ),
        )

    def __str__(self):
        return f'{self.user} -> {self.author}'
