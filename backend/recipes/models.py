from django.db import models
from django.core.validators import MinValueValidator
from users.models import FoodgramUser


class Tag(models.Model):
    """Модель для тегов"""
    name = models.CharField(null=False, max_length=200, verbose_name='Тэг')
    color = models.CharField(null=False, max_length=7, verbose_name='Цвет')
    slug = models.SlugField(null=False, max_length=200)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name', )

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    """Модель для ингридиентов"""
    name = models.CharField(
        max_length=200,
        verbose_name='Ингредиент'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Ед.измерения'
    )

    class Meta:
        verbose_name = 'Индрегиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name', )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель для рецептов"""
    author = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор'
    )

    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None,
        verbose_name='Фото'
        )
    text = models.TextField(
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        'Ingredients',
        related_name='recipe',
        through='IngredientsAmount'
    )
    favorite = models.ManyToManyField(
        FoodgramUser,
        verbose_name='Любимые рецепты',
        related_name='favorites'
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipe',
        verbose_name='Тэги'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления'
    )
    pub_date = models.DateTimeField(
        'Pub_date',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date', )

    def __str__(self):
        return self.name


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
