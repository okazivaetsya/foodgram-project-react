from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from recipes.models import (
    Tags, Recipes, Ingredients
)
from .serializers import TagsSerializer, RecipeSerializer, IngredientSerializer


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
