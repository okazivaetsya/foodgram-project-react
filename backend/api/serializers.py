from rest_framework import serializers
from recipes.models import Recipe, Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('name', 'color', 'slug')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags',
            'author', 'name',
            'image', 'text',
            'cooking_time'
        )
