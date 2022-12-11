from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя с переопределнным основным полем
    Основным полем является не 'username' а 'email'
    """
    email = models.EmailField('email', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username', 'password',
        'first_name', 'last_name',
    ]
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Follow(models.Model):
    """Модель для подписков на авторов"""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_following'
            )
        ]

    def __str__(self):
        return f'{self.user} -> {self.author}'
