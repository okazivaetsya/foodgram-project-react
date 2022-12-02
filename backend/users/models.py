from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='Подписчики'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='Автор'
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
