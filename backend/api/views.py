from django.shortcuts import get_list_or_404, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import Favorites, Ingredients, Recipes, ShoppingCart, Tags
from rest_framework import permissions, status, viewsets, serializers
from rest_framework.response import Response
from users.models import CustomUser, Follow
from .download_cart import DownloadCartView

from .filters import RecipeFilter, IngredientsFilter
from .pagination import FoodgramPagination
from .serializers import (FollowSerializer, IngredientSerializer,
                          RecipePostSerializer, RecipeSerializer,
                          SimpleRecipeSerializer, TagsSerializer,
                          UserSerializer)


class TagsViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с тегами"""
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с рецептами"""
    queryset = Recipes.objects.all()
    pagination_class = FoodgramPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        else:
            return RecipePostSerializer


class IngredientsViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с ингредиентами"""
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientsFilter


class CreateUserView(UserViewSet):
    """Вьюсет для работы с пользователями"""
    pagination_class = FoodgramPagination
    serializer_class = UserSerializer

    def get_queryset(self):
        return CustomUser.objects.all()


class FollowViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с подписками"""
    pagination_class = FoodgramPagination
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_list_or_404(CustomUser, following__user=self.request.user)

    def create(self, request, *args, **kwargs):
        author_id = self.kwargs.get('user_id')
        author = get_object_or_404(CustomUser, id=author_id)
        if author == request.user:
            raise serializers.ValidationError(
                {'errors': 'Нельзя подписываться на самого себя.'}
            )
        if self.request.user.follower.filter(author=author).exists():
            raise serializers.ValidationError(
                {'errors': 'Вы уже подписаны на данного автора.'}
            )
        else:
            Follow.objects.create(
                user=request.user, author=author
            )
            print(f'REQUEST = {request}')
            serializer = FollowSerializer(author, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        author_id = self.kwargs.get('user_id')
        user_id = request.user.id
        subscribe = get_object_or_404(
            Follow, user__id=user_id, author__id=author_id
        )
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с избранными рецептами"""
    serializer_class = SimpleRecipeSerializer
    queryset = Favorites.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipes, id=recipe_id)
        if Favorites.objects.filter(user=request.user, recipe=recipe).exists():
            raise serializers.ValidationError(
                {'errors': 'Данный рецепт уже в списке избранных рецептов.'}
            )
        else:
            Favorites.objects.create(user=request.user, recipe=recipe)
            serializer = SimpleRecipeSerializer(
                recipe, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        user_id = request.user.id
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(
            Favorites, user__id=user_id,
            recipe__id=recipe_id
        )
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы со списком покупок"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SimpleRecipeSerializer
    queryset = ShoppingCart.objects.all()

    def create(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipes, id=recipe_id)
        if ShoppingCart.objects.filter(
            user=request.user, recipe=recipe
        ).exists():
            raise serializers.ValidationError(
                {'errors': 'Данный рецепт уже добавлен в список покупок.'}
            )
        else:
            serializer = SimpleRecipeSerializer(recipe)
            ShoppingCart.objects.create(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        user_id = request.user.id
        recipe_id = self.kwargs.get('recipe_id')
        if not ShoppingCart.objects.filter(
            user__id=user_id,
            recipe__id=recipe_id
        ).exists():
            raise serializers.ValidationError(
                {'errors': 'Такого рецепта нет в списке покупок'}
            )
        else:
            recipe = get_object_or_404(
                ShoppingCart, user__id=user_id,
                recipe__id=recipe_id
            )
            recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class DownloadCart(DownloadCartView):
    permission_classes = [permissions.IsAuthenticated]
