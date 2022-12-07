from recipes.models import (
    Ingredients, IngredientsInRecipes,
    Recipes, Tags, Favorites, ShoppingCart,
    TagsInRecipes
)
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.models import CustomUser, Follow
from djoser.serializers import UserCreateSerializer
from users.services import check_user_items_in_models


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


class UserSerializer(UserCreateSerializer):
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
            'password'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (request.user.is_authenticated and Follow.objects.filter(
                    user=request.user,
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
    is_favorite = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
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
            'is_favorite',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        return check_user_items_in_models(Favorites, request, obj)

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return check_user_items_in_models(ShoppingCart, request, obj)


class RecipePostSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    author = UserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tags.objects.all(),
        many=True)
    ingredients = IngredientsInRecipeSerializer(
        source='ingredients_in_recipes', many=True)
    image = Base64ImageField(max_length=None, use_url=False,)

    class Meta:
        model = Recipes
        fields = ('id', 'author', 'name', 'image', 'text',
                  'ingredients', 'tags', 'cooking_time',
                  'is_in_shopping_cart', 'is_favorite')

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        return check_user_items_in_models(Favorites, request, obj)

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return check_user_items_in_models(ShoppingCart, request, obj)

    def add_tags_and_ingredients_to_recipe(
        self, tags, ingredients, recipe
    ):
        for tag in tags:
            recipe.tags.add(tag)
            recipe.save()
        for ingredient in ingredients:
            if not IngredientsInRecipes.objects.filter(
                    ingredient_id=ingredient['id'],
                    recipe=recipe).exists():
                new_ingredient_in_recipe = IngredientsInRecipes.objects.create(
                    ingredient_id=ingredient['id'],
                    recipe=recipe)
                new_ingredient_in_recipe.amount = ingredient['amount']
                new_ingredient_in_recipe.save()
            else:
                IngredientsInRecipes.objects.filter(
                    recipe=recipe).delete()
                recipe.delete()
                raise serializers.ValidationError(
                    'Неьзя добавлять один ингредиент дважды!')
        return recipe

    def create(self, validated_data):
        author = validated_data.get('author')
        tags = validated_data.pop('tags')
        name = validated_data.get('name')
        image = validated_data.get('image')
        text = validated_data.get('text')
        cooking_time = validated_data.get('cooking_time')
        ingredients = validated_data.pop('ingredients_in_recipes')
        recipe = Recipes.objects.create(
            author=author,
            name=name,
            image=image,
            text=text,
            cooking_time=cooking_time,
        )
        recipe = self.add_tags_and_ingredients_to_recipe(
            tags, ingredients, recipe
        )
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients_in_recipes')
        TagsInRecipes.objects.filter(recipe=instance).delete()
        IngredientsInRecipes.objects.filter(recipe=instance).delete()
        instance = self.add_tags_and_ingredients_to_recipe(
            tags, ingredients, instance)
        super().update(instance, validated_data)
        instance.save()
        return
