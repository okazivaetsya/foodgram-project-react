from djoser.views import UserViewSet
from recipes.models import Ingredients, Recipes, Tags
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from users.models import CustomUser

from .serializers import (IngredientSerializer, RecipeSerializer,
                          TagsSerializer, UserSerializer, RecipePostSerializer)


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
