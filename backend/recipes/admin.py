from django.contrib import admin

from .models import (Favorites, Ingredients, IngredientsInRecipes, Recipes,
                     ShoppingCart, Tags, TagsInRecipes)


class FoodgramAdminModel(admin.ModelAdmin):
    """Общая модель для админки"""
    empty_value_display = '-пусто-'


@admin.register(Tags)
class TagAdmin(FoodgramAdminModel):
    """Настройки для модели Тэгов"""
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug', 'color')


@admin.register(TagsInRecipes)
class TagsInRecipesAdmin(FoodgramAdminModel):
    """Настройки для модели Тегов в рецептах"""
    list_display = ('id', 'tag', 'recipe')
    search_fields = ('tag', 'recipe')
    list_filter = ('tag', 'recipe')


@admin.register(Ingredients)
class IngredientsAdmin(FoodgramAdminModel):
    """Настройки для модели Ингредиентов"""
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name', 'measurement_unit')
    list_filter = ('name', 'measurement_unit')


@admin.register(IngredientsInRecipes)
class IngredientsInRecipesAdmin(FoodgramAdminModel):
    """Настройки для модели Ингредиентов в рецептах"""
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    search_fields = ('recipe', 'ingredient')
    list_filter = ('recipe', 'ingredient')


@admin.register(Recipes)
class RecipesAdmin(FoodgramAdminModel):
    """Настройки для модели Рецептов"""
    list_display = (
        'id', 'name',
        'image', 'cooking_time',
        'text', 'pub_date', 'favorites_count'
    )

    def favorites_count(self, obj):
        return obj.favorites.all().count()

    favorites_count.short_description = "кол-во добавлений в избранное"


@admin.register(Favorites)
class FavoriteRecipesAdmin(FoodgramAdminModel):
    """Настройки для модели избранных рецептов"""
    list_display = (
        'user', 'recipe'
    )
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(FoodgramAdminModel):
    """Настройки для модели Списка покупок"""
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')
