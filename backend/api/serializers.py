from rest_framework import serializers
from recipes.models import Recipe, Tag, User, IngredientsAmount, Ingredients


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для Тегов"""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя"""
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class IngredientInRecipesSerializer(serializers.ModelSerializer):
    """Сериализатор для показа ингредиентов в рецепте"""
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit")

    class Meta:
        model = IngredientsAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов"""
    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов"""
    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientInRecipesSerializer(
        source='ingredients_amount',
        many=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )
