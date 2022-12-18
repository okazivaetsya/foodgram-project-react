from djoser.serializers import UserCreateSerializer
from drf_extra_fields.fields import Base64ImageField
from drf_writable_nested import WritableNestedModelSerializer

from recipes.models import (
    Favorites, Ingredients, IngredientsInRecipes,
    Recipes, ShoppingCart, Tags, TagsInRecipes
)
from rest_framework import serializers
from users.models import CustomUser, Follow
from users.utils import check_user_items_in_models


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
        """Метод проверяет является ли пользорватель подписаным на автора"""
        request = self.context.get('request')
        return (request.user.is_authenticated and Follow.objects.filter(
                    user=request.user,
                    author=obj
                ).exists())


class IngredientForRecipePostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображдения ингредиентов
    при реализации POST метода на эндпоинте recipes
    """
    id = serializers.IntegerField(source='ingredient.id')

    class Meta:
        model = IngredientsInRecipes
        fields = ('id', 'amount')


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
    is_favorited = serializers.SerializerMethodField(read_only=True)
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
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        """Метод проверяет является ли рецепт любимым(избранным)"""
        request = self.context.get('request')
        return check_user_items_in_models(Favorites, request, obj)

    def get_is_in_shopping_cart(self, obj):
        """Метод проверяет добавлен ли рецепт списко покупок"""
        request = self.context.get('request')
        return check_user_items_in_models(ShoppingCart, request, obj)


class RecipePostSerializer(
    WritableNestedModelSerializer, serializers.ModelSerializer
):
    """Сериализатор для Рецептов для метода POST"""
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tags.objects.all(),
        many=True)
    ingredients = IngredientForRecipePostSerializer(
        source='ingredients_in_recipes', many=True)
    image = Base64ImageField(max_length=None, use_url=False,)

    class Meta:
        model = Recipes
        fields = ('id', 'author', 'name', 'image', 'text',
                  'ingredients', 'tags', 'cooking_time',
                  'is_in_shopping_cart', 'is_favorited')

    def get_is_favorited(self, obj):
        """Метод проверяет является ли рецепт любимым(избранным)"""
        request = self.context.get('request')
        return check_user_items_in_models(Favorites, request, obj)

    def get_is_in_shopping_cart(self, obj):
        """Метод проверяет добавлен ли рецепт списко покупок"""
        request = self.context.get('request')
        return check_user_items_in_models(ShoppingCart, request, obj)

    @staticmethod
    def __add_tags_and_ingredients_to_recipe(
        tags, ingredients, recipe
    ):
        """Метод добавляет тэги и ингредиенты к основным полям рецептов"""
        for tag in tags:
            recipe.tags.add(tag)
            recipe.save()
        IngredientsInRecipes.objects.bulk_create(
            [IngredientsInRecipes(
                ingredient_id=ingredient['ingredient']['id'],
                recipe=recipe,
                amount=ingredient['amount']
            ) for ingredient in ingredients]
        )
        return recipe

    def create(self, validated_data):
        author = validated_data.get('author')
        tags = validated_data.get('tags')
        name = validated_data.get('name')
        image = validated_data.get('image')
        text = validated_data.get('text')
        cooking_time = validated_data.get('cooking_time')
        ingredients = validated_data.get('ingredients_in_recipes')
        recipe = Recipes.objects.create(
            author=author,
            name=name,
            image=image,
            text=text,
            cooking_time=cooking_time,
        )
        return self.__add_tags_and_ingredients_to_recipe(
            tags, ingredients, recipe
        )

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients_in_recipes')
        TagsInRecipes.objects.filter(recipe=instance).delete()
        IngredientsInRecipes.objects.filter(recipe=instance).delete()
        instance = self.__add_tags_and_ingredients_to_recipe(
            tags, ingredients, instance)
        super().update(instance, validated_data)
        instance.save()
        return instance


class SimpleRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для Рецептов для эндпоинта subscriptions
    Достаем только поля id, name, cooking_time, image
    """

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'cooking_time', 'image')

    def validate(self, data):
        if ShoppingCart.objects.filter(
                user=self.context.get('request').user,
                recipe=data['id']
        ).exists():
            raise serializers.ValidationError({
                'errors': 'Рецепт уже добавлен в список покупок.'
            })
        return data


class FavoriteSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipes.objects.all()
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all()
    )

    class Meta:
        model = Favorites
        fields = ('user', 'recipe')

    def validate(self, data):
        if Favorites.objects.filter(
                user=self.context.get('request').user,
                recipe=data['id']
        ).exists():
            raise serializers.ValidationError({
                'errors': 'Рецепт уже добавлен в избранное.'
            })
        return data

    def to_representation(self, instance):
        return SimpleRecipeSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок"""
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        """Метод проверяет подписан ли пользователь на автора"""
        request = self.context.get('request')
        return (
            request.user.is_authenticated and Follow.objects.filter(
                user=request.user,
                author=obj
            ).exists()
        )

    def get_recipes_count(self, obj):
        """метод подсчитыает кол-во рецептов у данного автора"""
        return Recipes.objects.filter(author__id=obj.id).count()

    def get_recipes(self, obj):
        """метод достает рецепты с учетом query параметра recipes_limit"""
        request = self.context.get('request')
        recipes_limit = request.GET.get('recipes_limit')
        queryset = Recipes.objects.filter(
                author__id=obj.id).order_by('id')
        if recipes_limit:
            return SimpleRecipeSerializer(
                queryset[:recipes_limit], many=True
            ).data
        return SimpleRecipeSerializer(queryset, many=True).data

    def validate(self, data):
        if Follow.objects.filter(
                user=self.context.get('request').user,
                author=data['id']
        ).exists():
            raise serializers.ValidationError({
                'errors': 'Вы уже подписаны на данного автора.'
            })

        if self.context.get('request').user.id == data['id']:
            raise serializers.ValidationError({
                'errors': 'Нельзя подписываться на самого себя'
            })
        return data
