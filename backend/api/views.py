from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from recipes.models import Recipe, Ingredients, Tag
from .serializers import (
    RecipeSerializer, IngredientSerializer,
    TagSerializer, UserSerializer)
from django.contrib.auth import get_user_model

User = get_user_model()


class RecipesViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticatedOrReadOnly, )


class IngredientsViewSet(ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class TagsViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )
