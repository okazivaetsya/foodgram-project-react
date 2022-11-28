from rest_framework.viewsets import ModelViewSet
from recipes.models import Recipe
from .serializers import RecipeSerializer


class RecipesViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
