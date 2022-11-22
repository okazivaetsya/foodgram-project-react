from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()


class Tag(models.Model):
    """Модель для тегов"""
    title = models.CharField(null=False, max_length=200)
    color = models.CharField(null=False, max_length=200)
    slug = models.SlugField(null=False, max_length=200)

    class Meta:
        ordering = ('title', )

    def __str__(self):
        return self.title


class Ingredients(models.Model):
    """Модель для ингридиентов"""
    title = models.CharField(max_length=200)
    unit = models.CharField(max_length=200)

    class Meta:
        ordering = ('title', )

    def __str__(self):
        return self.title


class Recipe(models.Model):
    """Модель для рецептов"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='author'
    )

    title = models.CharField(max_length=200)
    picture = models.ImageField(
        upload_to='recipe/images/',
        null=True,
        default=None
        )
    description = models.TextField()
    ingredients = models.ManyToManyField(
        'Ingredients',
        related_name='recipe',
        through='IngredientsAmount'
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipe'
    )
    cooking_time = models.IntegerField()

    pub_date = models.DateTimeField(
        'Pub_date',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date', )

    def __str__(self):
        return self.title


class IngredientsAmount(models.Model):
    """Модель для посчета кол-ва ингредиентов"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_amount'
    )
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.SET_NULL,
        null=True,
        related_name='ingredients_amount'
    )
    amount = models.PositiveIntegerField(
        default=None,
        validators=[
            MinValueValidator(1)
        ]
    )

    class Meta:
        ordering = ('ingredient', )

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'
