from django.contrib import admin
from .models import Recipe, Ingredients, IngredientsAmount, Tag


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'picture',
        'description',
        'cooking_time',
        'pub_date',)
    search_fields = ('description', 'title',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'


class IngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'unit',
       )
    search_fields = ('title',)
    list_filter = ('unit',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'color',
        'slug',
    )


class IngredientsAmountAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'amount',
    )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(IngredientsAmount, IngredientsAmountAdmin)
