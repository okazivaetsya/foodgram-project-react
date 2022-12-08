from rest_framework import status
from django.shortcuts import get_list_or_404, get_object_or_404
from djoser.views import UserViewSet
from rest_framework.response import Response
from recipes.models import Ingredients, Recipes, Tags, Favorites, ShoppingCart
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from users.models import CustomUser, Follow

from .serializers import (IngredientSerializer, RecipeSerializer,
                          TagsSerializer, UserSerializer, RecipePostSerializer,
                          FollowSerializer, RecipeInSubscriptionSerializer)


class TagsViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с тегами"""
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с рецептами"""
    queryset = Recipes.objects.all()
    pagination_class = PageNumberPagination

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
    pagination_class = None


class CreateUserView(UserViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return CustomUser.objects.all()


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer

    def get_queryset(self):
        return get_list_or_404(CustomUser, following__user=self.request.user)

    def create(self, request, *args, **kwargs):
        author_id = self.kwargs.get('user_id')
        author = get_object_or_404(CustomUser, id=author_id)
        Follow.objects.create(
            user=request.user, author=author
        )
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        print(f'self.kwargs = {self.kwargs}')
        author_id = self.kwargs.get('user_id')
        print(f'author_id = {author_id}')
        user_id = request.user.id
        print(f'user = {request.user}')
        subscribe = get_object_or_404(
            Follow, user__id=user_id, author__id=author_id
        )
        print(f'subscribe = {subscribe}')
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeInSubscriptionSerializer

    def get_queryset(self):
        return get_list_or_404(Recipes, Favorites__user=self.request.user)

    def create(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipes, id=recipe_id)
        Favorites.objects.create(user=request.user, recipe=recipe)
        return Response(status=status.HTTP_201_CREATED)

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
    serializer_class = RecipeInSubscriptionSerializer

    def get_queryset(self):
        return get_list_or_404(Recipes, shopping_cart__user=self.request.user)

    def create(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipes, id=recipe_id)
        ShoppingCart.objects.create(user=request.user, recipe=recipe)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        user_id = request.user.id
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(
            ShoppingCart, user__id=user_id,
            recipe__id=recipe_id
        )
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
