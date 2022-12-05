from rest_framework import serializers
from recipes.models import Tags, Recipes, Ingredients, IngredientsInRecipes
from users.models import CustomUser, Follow


class TagsSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов"""

    class Meta:
        model = Tags
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода данных пользоваетля"""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):  # заработает как прикрутим аутетификацию
        request = self.context.get('request')
        return (request.user.is_authenticated and Follow.objects.filter(
                    user=self.context['request'].user,
                    author=obj
                ).exists())


class IngredientsInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для кол-ва ингредиентов в рецептах"""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientsInRecipes
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов"""
    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов"""
    tags = TagsSerializer(many=True)
    ingredients = IngredientsInRecipeSerializer(
        source='ingredients_in_recipes',
        many=True
    )
    author = UserSerializer()

    class Meta:
        model = Recipes
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
