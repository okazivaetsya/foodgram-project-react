from django.contrib import admin
from users.models import Follow
from .models import (
    Tags, TagsInRecipes, Recipes, Ingredients,
    IngredientsInRecipes, ShoppingCart
)


class FoodgramAdminModel(admin.ModelAdmin):
    empty_value_display = '-пусто-'


class TagAdmin(FoodgramAdminModel):
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug', 'color')


class TagsInRecipesAdmin(FoodgramAdminModel):
    list_display = ('id', 'tag', 'recipe')
    search_fields = ('tag', 'recipe')
    list_filter = ('tag', 'recipe')


class IngredientsAdmin(FoodgramAdminModel):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name', 'measurement_unit')
    list_filter = ('name', 'measurement_unit')


class IngredientsInRecipesAdmin(FoodgramAdminModel):
    list_display = ('id', 'recipe', 'ingredient')
    search_fields = ('recipe', 'ingredient')
    list_filter = ('recipe', 'ingredient')


class RecipesAdmin(FoodgramAdminModel):
    list_display = (
        'id', 'name',
        'image', 'cooking_time',
        'text', 'pub_date',
    )
    empty_value_display = '-пусто-'


class FollowAdmin(FoodgramAdminModel):
    list_display = ('id', 'user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')


class ShoppingCartAdmin(FoodgramAdminModel):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')


admin.site.register(Tags, TagAdmin)
admin.site.register(TagsInRecipes, TagsInRecipesAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(IngredientsInRecipes, IngredientsInRecipesAdmin)
admin.site.register(Recipes, RecipesAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
