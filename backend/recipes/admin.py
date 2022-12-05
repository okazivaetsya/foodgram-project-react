from django.contrib import admin
from users.models import Follow
from .models import (
    Tags, TagsInRecipes, Recipes, Ingredients,
    IngredientsInRecipes, ShoppingCart
)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug', 'color')
    empty_value_display = '-пусто-'


class TagsInRecipesAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'recipe')
    search_fields = ('tag', 'recipe')
    list_filter = ('tag', 'recipe')
    empty_value_display = '-пусто-'


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name', 'measurement_unit')
    list_filter = ('name', 'measurement_unit')
    empty_value_display = '-пусто-'


class IngredientsInRecipesAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient')
    search_fields = ('recipe', 'ingredient')
    list_filter = ('recipe', 'ingredient')
    empty_value_display = '-пусто-'


class RecipesAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name',
        'image', 'cooking_time',
        'text', 'pub_date',
    )
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')
    empty_value_display = '-пусто-'


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    empty_value_display = '-пусто-'


admin.site.register(Tags, TagAdmin)
admin.site.register(TagsInRecipes, TagsInRecipesAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(IngredientsInRecipes, IngredientsInRecipesAdmin)
admin.site.register(Recipes, RecipesAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
