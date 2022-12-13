from django.core.validators import MinValueValidator
from django.db import models
from users.models import CustomUser


class Tags(models.Model):
    """Модель для тэгов"""
    name = models.CharField(max_length=200, verbose_name='Тэг')
    color = models.CharField(max_length=7, verbose_name='Цвет')
    slug = models.SlugField(max_length=200, verbose_name='slug')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self) -> str:
        return self.name


class Ingredients(models.Model):
    """Модель для ингредиентов"""
    name = models.CharField(
        max_length=200,
        verbose_name='Наименование'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient'
            )
        ]

    def __str__(self) -> str:
        return f'{self.name}: {self.measurement_unit}'


class TagsInRecipes(models.Model):
    """Модель для тегов в рецептах"""
    tag = models.ForeignKey(
        'Tags',
        on_delete=models.CASCADE,
        related_name='tag_in_recipes',
        verbose_name='Тэг'
    )
    recipe = models.ForeignKey(
        'Recipes',
        on_delete=models.CASCADE,
        related_name='tag_in_recipes',
        verbose_name='Рецепт'
    )

    class Meta:
        ordering = ('recipe',)
        verbose_name = 'Тэг в рецептах'
        verbose_name_plural = 'Тэги в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=('tag', 'recipe', ),
                name='unique_tag'
            )
        ]

    def __str__(self) -> str:
        return f'{self.recipe}: {self.tag}'


class Recipes(models.Model):
    """Модель для рецептов"""
    name = models.CharField(
        verbose_name='Название',
        max_length=200
    )
    image = models.ImageField(
        verbose_name='фото',
        upload_to='recipes/images',
        null=True
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[
            MinValueValidator(
                1,
                message='Значение должно быть больше 1'
            )
        ]
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    tags = models.ManyToManyField(
        'Tags',
        through='TagsInRecipes',
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        'Ingredients',
        through='IngredientsInRecipes',
        related_name='recipes'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date', )

    def __str__(self) -> str:
        return self.name


class IngredientsInRecipes(models.Model):
    """Модель для ингредиентов в рецептах"""
    recipe = models.ForeignKey(
        'Recipes',
        on_delete=models.CASCADE,
        related_name='ingredients_in_recipes',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        'Ingredients',
        on_delete=models.CASCADE,
        related_name='ingredients_in_recipes',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1, 'Минимальное значение для поля - 1')]
    )

    class Meta:
        ordering = ('recipe',)
        verbose_name_plural = 'Ингредиенты в рецепте'
        constraints = [
            models.UniqueConstraint(
                fields=('ingredient', 'recipe', ),
                name='unique_ingredients_in_recipe'
            )
        ]

    def __str__(self) -> str:
        return f'{self.recipe}: {self.ingredient}'


class Favorites(models.Model):
    """Модель для хранения избранных рецептов"""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='Favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        'Recipes',
        on_delete=models.CASCADE,
        related_name='Favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Любимый рецепт'
        verbose_name_plural = 'Любимые рецепты'
        ordering = ('user',)
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite'
            )
        ]

    def __str__(self) -> str:
        return f'{self.user}: {self.recipe}'


class ShoppingCart(models.Model):
    """Модель для хранения списка покупок"""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        'Recipes',
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        ordering = ('user',)
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_cart'
            )
        ]
